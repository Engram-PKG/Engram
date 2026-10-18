import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import func, select
from voyageai.error import RateLimitError

import app.services.ingestion.sync as sync_module
import app.services.ingestion.uploads as uploads_module
from app.core.config import get_settings
from app.db.session import async_session_factory
from app.main import app
from app.models.memory_item import EMBEDDING_DIM, MemoryItem
from app.models.upload import Upload
from app.services.ingestion import documents, voice_notes
from app.services.ingestion.bookmarks import parse_bookmarks

PASSWORD = "correct-horse-battery"


@pytest.fixture(autouse=True)
def embed_calls(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Every test gets a fake embedder; the returned list logs each call's input texts."""
    calls: list[list[str]] = []

    async def fake_embed(texts: list[str]) -> list[list[float]]:
        calls.append(texts)
        return [[0.1] * EMBEDDING_DIM for _ in texts]

    monkeypatch.setattr(sync_module, "embed_texts", fake_embed)
    return calls


@asynccontextmanager
async def _signed_up_client() -> AsyncIterator[tuple[AsyncClient, uuid.UUID]]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        signup = await client.post(
            "/api/v1/auth/signup",
            json={"email": f"{uuid.uuid4()}@example.com", "password": PASSWORD},
        )
        yield client, uuid.UUID(signup.json()["id"])


async def _upload(
    client: AsyncClient,
    filename: str,
    data: bytes,
    content_type: str = "application/octet-stream",
    **form: str,
) -> Response:
    return await client.post(
        "/api/v1/uploads/", files={"file": (filename, data, content_type)}, data=form
    )


def _pdf(pages: list[str], creation_date: str | None = None) -> bytes:
    """A minimal valid PDF with one line of Helvetica text per page."""
    page_ids = [4 + 2 * i for i in range(len(pages))]
    info_id = 4 + 2 * len(pages)
    kids = " ".join(f"{p} 0 R" for p in page_ids)
    objects: dict[int, bytes] = {
        1: b"<< /Type /Catalog /Pages 2 0 R >>",
        2: f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode(),
        3: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        info_id: (
            f"<< /CreationDate (D:{creation_date}) >>".encode() if creation_date else b"<< >>"
        ),
    }
    for page_id, text in zip(page_ids, pages, strict=True):
        stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode() if text else b""
        objects[page_id] = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % (page_id + 1)
        )
        objects[page_id + 1] = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream)

    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for object_id in sorted(objects):
        offsets[object_id] = len(out)
        out += b"%d 0 obj\n%s\nendobj\n" % (object_id, objects[object_id])
    xref_at = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (info_id + 1)
    for object_id in range(1, info_id + 1):
        out += b"%010d 00000 n \n" % offsets[object_id]
    out += b"trailer\n<< /Size %d /Root 1 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        info_id + 1,
        info_id,
        xref_at,
    )
    return bytes(out)


def _bookmark_export(*links: str) -> bytes:
    return (
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
        "<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n"
        + "\n".join(links)
        + "\n</DL><p>\n"
    ).encode()


async def _memories(user_id: uuid.UUID, source: str | None = None) -> list[MemoryItem]:
    async with async_session_factory() as db:
        stmt = select(MemoryItem).where(MemoryItem.user_id == user_id)
        if source:
            stmt = stmt.where(MemoryItem.source == source)
        return list((await db.execute(stmt.order_by(MemoryItem.external_id))).scalars())


async def _upload_count(user_id: uuid.UUID) -> int:
    async with async_session_factory() as db:
        return await db.scalar(select(func.count()).where(Upload.user_id == user_id)) or 0


# --- parsing units -----------------------------------------------------------------------


def test_chunk_text_keeps_paragraphs_and_overlaps() -> None:
    paragraphs = [f"Paragraph {i}. " + "word " * 150 for i in range(12)]
    chunks = documents.chunk_text("\n\n".join(paragraphs))

    assert len(chunks) > 1
    assert all(len(chunk) <= 2400 for chunk in chunks)
    # Every paragraph made it into some chunk, and each chunk starts with the previous
    # chunk's tail.
    joined = "\n".join(chunks)
    assert all(f"Paragraph {i}." in joined for i in range(12))
    for previous, current in zip(chunks, chunks[1:], strict=False):
        assert current.split("\n\n")[0] in previous


def test_chunk_text_splits_a_single_huge_token() -> None:
    chunks = documents.chunk_text("x" * 5000)
    assert "".join(chunks).count("x") >= 5000
    assert all(len(chunk) <= 2400 for chunk in chunks)


def test_parse_bookmarks_folders_dates_and_filtering() -> None:
    html = _bookmark_export(
        '<DT><H3 ADD_DATE="1600000000">Work</H3>',
        "<DL><p>",
        '<DT><H3>Docs</H3><DL><p><DT><A HREF="https://docs.example.com" ADD_DATE="1700000000">'
        "Team docs</A></DL><p>",
        '<DT><A HREF="https://jira.example.com" ADD_DATE="1700000000000">Jira</A>',
        "</DL><p>",
        '<DT><A HREF="javascript:alert(1)">Bookmarklet</A>',
        '<DT><A HREF="https://news.example.com">News</A>',
        '<DT><A HREF="https://news.example.com">News again</A>',
    ).decode()

    bookmarks = parse_bookmarks(html)

    assert [(b.title, b.folder) for b in bookmarks] == [
        ("Team docs", "Work / Docs"),
        ("Jira", "Work"),
        ("News", ""),
    ]
    assert bookmarks[0].added_at == datetime.fromtimestamp(1700000000, tz=UTC)
    # Milliseconds are normalised to the same instant.
    assert bookmarks[1].added_at == bookmarks[0].added_at
    assert bookmarks[2].added_at is None


# --- API -----------------------------------------------------------------------------------


async def test_upload_routes_require_auth() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        assert (await _upload(client, "a.txt", b"hi")).status_code == 401
        assert (await client.get("/api/v1/uploads/")).status_code == 401


async def test_text_upload_is_indexed_and_linked(embed_calls: list[list[str]]) -> None:
    async with _signed_up_client() as (client, user_id):
        response = await _upload(
            client,
            "notes/ideas.md",
            b"# Ideas\n\nBuild a twin.",
            "text/markdown",
            occurred_at="2024-03-01T09:00:00Z",
        )

    assert response.status_code == 201
    body = response.json()
    assert body["kind"] == "document"
    assert body["filename"] == "ideas.md"  # client-supplied directories are stripped
    assert body["items"] == 1

    [item] = await _memories(user_id)
    assert item.source == "document"
    assert str(item.upload_id) == body["id"]
    assert item.content == "ideas.md\n\n# Ideas\n\nBuild a twin."
    assert item.embedding is not None
    assert item.occurred_at == datetime(2024, 3, 1, 9, tzinfo=UTC)
    assert embed_calls == [[item.content]]


async def test_pdf_upload_uses_pdf_creation_date_and_counts_pages() -> None:
    pdf = _pdf(["Certificate of Completion", "Awarded to Yashi"], creation_date="20230615120000Z")
    async with _signed_up_client() as (client, user_id):
        response = await _upload(
            client, "cert.pdf", pdf, "application/pdf", occurred_at="2026-01-01T00:00:00Z"
        )

    assert response.status_code == 201, response.text
    assert response.json()["details"] == {"pages": 2, "truncated": False}
    [item] = await _memories(user_id)
    assert "Certificate of Completion" in item.content
    assert "Awarded to Yashi" in item.content
    assert item.item_metadata["pages"] == 2
    # The PDF's own date wins over the browser's last-modified time.
    assert item.occurred_at == datetime(2023, 6, 15, 12, tzinfo=UTC)


async def test_long_document_is_chunked_but_shown_once_on_the_timeline() -> None:
    text = "\n\n".join(f"Section {i}. " + "detail " * 200 for i in range(10))
    text += "\n\nThe needle is here."
    async with _signed_up_client() as (client, user_id):
        response = await _upload(client, "report.txt", text.encode())
        count = response.json()["items"]
        browse = (await client.get("/api/v1/memory/timeline")).json()
        search = (await client.get("/api/v1/memory/timeline", params={"q": "needle"})).json()

    assert count > 1
    chunks = await _memories(user_id)
    assert len(chunks) == count
    assert chunks[0].content.startswith(f"report.txt (part 1 of {count})\n\n")

    [entry] = browse["items"]
    assert entry["details"]["chunk_index"] == 0
    assert entry["details"]["chunk_count"] == count
    assert browse["sources"] == [{"source": "document", "count": 1}]
    # A search surfaces the chunk that actually matches, not just the first.
    [hit] = search["items"]
    assert hit["details"]["chunk_index"] == count - 1


async def test_rejected_uploads(monkeypatch: pytest.MonkeyPatch) -> None:
    async with _signed_up_client() as (client, user_id):
        unsupported = await _upload(client, "photo.png", b"\x89PNG....")
        plain_html = await _upload(client, "page.html", b"<html><body>hi</body></html>")
        empty = await _upload(client, "empty.txt", b"")
        binary = await _upload(client, "fake.txt", b"abc\x00def")
        scanned = await _upload(client, "scan.pdf", _pdf([""]))
        damaged = await _upload(client, "broken.pdf", b"%PDF-1.4 garbage")
        monkeypatch.setattr(get_settings(), "upload_max_bytes", 10)
        too_big = await _upload(client, "big.txt", b"x" * 11)

    assert unsupported.status_code == 415
    assert plain_html.status_code == 415
    assert "bookmark" in plain_html.json()["detail"]
    assert empty.status_code == 422
    assert binary.status_code == 422
    assert scanned.status_code == 422
    assert "scanned" in scanned.json()["detail"]
    assert damaged.status_code == 422
    assert too_big.status_code == 413
    assert await _upload_count(user_id) == 0
    assert await _memories(user_id) == []


async def test_same_file_twice_conflicts() -> None:
    async with _signed_up_client() as (client, user_id):
        first = await _upload(client, "a.txt", b"same bytes")
        second = await _upload(client, "renamed.txt", b"same bytes")

    assert first.status_code == 201
    assert second.status_code == 409
    assert "a.txt" in second.json()["detail"]
    assert len(await _memories(user_id)) == 1


async def test_embedding_failure_stores_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0

    async def flaky_embed(texts: list[str]) -> list[list[float]]:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RateLimitError("slow down")
        return [[0.1] * EMBEDDING_DIM for _ in texts]

    monkeypatch.setattr(sync_module, "embed_texts", flaky_embed)
    async with _signed_up_client() as (client, user_id):
        response = await _upload(client, "a.txt", b"hello")
        # The failed attempt must not block a retry as a "duplicate".
        retry = await _upload(client, "a.txt", b"hello")

    assert response.status_code == 502
    assert retry.status_code == 201
    assert await _upload_count(user_id) == 1


async def test_voice_note_is_transcribed(monkeypatch: pytest.MonkeyPatch) -> None:
    received: list[tuple[str, bytes]] = []

    async def fake_transcribe(filename: str, data: bytes) -> str:
        received.append((filename, data))
        return "Remind me to send the NOC to Aditya on Friday."

    monkeypatch.setattr(voice_notes, "transcribe", fake_transcribe)
    async with _signed_up_client() as (client, user_id):
        response = await _upload(
            client, "memo.m4a", b"fake-audio", "audio/mp4", occurred_at="2026-09-20T18:30:00Z"
        )

    assert response.status_code == 201
    assert response.json()["kind"] == "voice_note"
    assert received == [("memo.m4a", b"fake-audio")]
    [item] = await _memories(user_id)
    assert item.source == "voice_note"
    assert item.content == "memo.m4a\n\nRemind me to send the NOC to Aditya on Friday."
    assert item.occurred_at == datetime(2026, 9, 20, 18, 30, tzinfo=UTC)


async def test_voice_note_transcription_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def failing_transcribe(filename: str, data: bytes) -> str:
        raise voice_notes.TranscriptionFailed("groq down")

    monkeypatch.setattr(voice_notes, "transcribe", failing_transcribe)
    async with _signed_up_client() as (client, user_id):
        response = await _upload(client, "memo.mp3", b"fake-audio")

    assert response.status_code == 502
    assert await _upload_count(user_id) == 0


async def test_bookmark_reimport_updates_instead_of_duplicating(
    embed_calls: list[list[str]],
) -> None:
    old_export = _bookmark_export(
        '<DT><A HREF="https://a.example.com" ADD_DATE="1600000000">A</A>',
        '<DT><A HREF="https://b.example.com" ADD_DATE="1600000000">B</A>',
    )
    new_export = _bookmark_export(
        '<DT><A HREF="https://a.example.com" ADD_DATE="1600000000">A</A>',
        '<DT><A HREF="https://b.example.com" ADD_DATE="1600000000">B</A>',
        '<DT><A HREF="https://c.example.com" ADD_DATE="1700000000">C</A>',
    )
    async with _signed_up_client() as (client, user_id):
        first = await _upload(client, "bookmarks_old.html", old_export, "text/html")
        second = await _upload(client, "bookmarks_new.html", new_export, "text/html")
        listing = (await client.get("/api/v1/uploads/")).json()

    assert first.json()["kind"] == "bookmark"
    assert first.json()["details"] == {"bookmarks": 2}
    items = await _memories(user_id, "bookmark")
    assert sorted(i.item_metadata["url"] for i in items) == [
        "https://a.example.com",
        "https://b.example.com",
        "https://c.example.com",
    ]
    new_id = second.json()["id"]
    assert {str(i.upload_id) for i in items} == {new_id}
    # Unchanged bookmarks are not re-embedded on re-import.
    assert [len(call) for call in embed_calls] == [2, 1]
    assert {u["filename"]: u["items"] for u in listing} == {
        "bookmarks_new.html": 3,
        "bookmarks_old.html": 0,
    }


async def test_list_download_delete_and_ownership() -> None:
    async with _signed_up_client() as (client, user_id):
        created = (await _upload(client, "resume.txt", b"Yashi - Engineer")).json()
        await _upload(client, "other.txt", b"Something else")
        listing = (await client.get("/api/v1/uploads/")).json()
        download = await client.get(f"/api/v1/uploads/{created['id']}/file")

        async with _signed_up_client() as (stranger, _):
            assert (await stranger.get(f"/api/v1/uploads/{created['id']}/file")).status_code == 404
            assert (await stranger.delete(f"/api/v1/uploads/{created['id']}")).status_code == 404

        deleted = await client.delete(f"/api/v1/uploads/{created['id']}")
        missing = await client.delete(f"/api/v1/uploads/{created['id']}")

    assert [u["filename"] for u in listing] == ["other.txt", "resume.txt"]
    assert download.status_code == 200
    assert download.content == b"Yashi - Engineer"
    assert download.headers["content-type"] == "application/octet-stream"
    assert "resume.txt" in download.headers["content-disposition"]
    assert deleted.status_code == 204
    assert missing.status_code == 404
    assert [m.item_metadata["filename"] for m in await _memories(user_id)] == ["other.txt"]


async def test_forget_and_reset_remove_uploaded_files() -> None:
    async with _signed_up_client() as (client, user_id):
        await _upload(client, "a.txt", b"document one")
        await _upload(
            client,
            "bookmarks.html",
            _bookmark_export('<DT><A HREF="https://a.example.com">A</A>'),
        )
        forget = await client.delete("/api/v1/account/memories", params={"source": "document"})
        remaining_kinds = [u["kind"] for u in (await client.get("/api/v1/uploads/")).json()]
        export = (await client.get("/api/v1/account/export")).json()
        reset = await client.post("/api/v1/account/reset", json={"password": PASSWORD})

    assert forget.json() == {"deleted": 1}
    assert remaining_kinds == ["bookmark"]
    assert [u["filename"] for u in export["uploads"]] == ["bookmarks.html"]
    assert reset.status_code == 204
    assert await _upload_count(user_id) == 0
    assert await _memories(user_id) == []


def test_detect_kind_sniffs_pdf_without_extension() -> None:
    assert uploads_module.detect_kind("download", b"%PDF-1.7 ...") == ("document", "pdf")
