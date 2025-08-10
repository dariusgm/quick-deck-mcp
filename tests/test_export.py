import asyncio
import glob
import json
import os
from time import sleep
import pytest
import shutil
from global_settings import TEMP_DIR
from export import export

import pytest
import os
import asyncio
import json
from shutil import copy
from export import export
from global_settings import TEMP_DIR


@pytest.fixture
def setup_markdown_file(request):
    job_id = request.param
    src_file = f"tests/git_big.md"
    dest_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    shutil.copy(src_file, dest_file)
    yield job_id


@pytest.mark.asyncio
@pytest.mark.parametrize("setup_markdown_file,export_format", [
    ("test_rtf", "rtf"),
    ("test_pptx", "pptx"),
    ("test_html", "html"),
    ("test_pdf", "pdf")], indirect=["setup_markdown_file"])
async def test_export(setup_markdown_file, export_format):
    await export(setup_markdown_file, export_format=export_format)
    assert os.path.exists(os.path.join(TEMP_DIR, f"{setup_markdown_file}.{export_format}"))
    with open(os.path.join(TEMP_DIR, f"{setup_markdown_file}.json"), "r") as f:
        parsed = json.load(f)
        assert parsed["export_format"] == export_format
        assert parsed["status"] == "done"

    for f in glob.glob(os.path.join(TEMP_DIR, "test_*")):
        os.remove(f)

def test_export_performance():
    """
    Test function to ensure performance of export functions.
    This is a placeholder for actual performance test logic.
    """
    shutil.copy("tests/git_big.md", os.path.join(TEMP_DIR, "test_pdf.md"))
    job_id = "test_pdf"
    asyncio.run(export(job_id, export_format="pdf"))
    assert os.path.exists(os.path.join(TEMP_DIR, "test_pdf.md"))
    assert os.path.exists(os.path.join(TEMP_DIR, "test_pdf_clean.md"))
    assert os.path.exists(os.path.join(TEMP_DIR, "test_pdf.pdf"))
    with open(os.path.join(TEMP_DIR, "test_pdf.json"), "r") as f:
        parsed = json.load(f)
        assert parsed["export_format"] == "pdf"
        assert parsed["status"] == "done"
