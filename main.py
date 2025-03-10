from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Tuple, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.staticfiles import StaticFiles

# Database configuration using SQLite.
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Assessment model to store form submissions.
class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    battalion = Column(String, nullable=True)
    oic_name = Column(String, nullable=True)
    aoic_name = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    planned_start = Column(String, nullable=True)
    planned_completion = Column(String, nullable=True)
    actual_completion = Column(String, nullable=True)
    final_score = Column(Integer, nullable=True)
    final_percentage = Column(Float, nullable=True)
    errors = Column(Text, nullable=True)
    signature_oic = Column(Text, nullable=True)
    signature_ncr = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Comment fields for each assessment item.
    comment_item1 = Column(Text, nullable=True)
    comment_item2 = Column(Text, nullable=True)
    comment_item3 = Column(Text, nullable=True)
    comment_item4 = Column(Text, nullable=True)
    comment_item5 = Column(Text, nullable=True)
    comment_item6 = Column(Text, nullable=True)
    comment_item78 = Column(Text, nullable=True)  # Combined comments for Items 7 & 8.
    comment_item9 = Column(Text, nullable=True)
    comment_item10 = Column(Text, nullable=True)
    comment_item11 = Column(Text, nullable=True)
    comment_item12 = Column(Text, nullable=True)
    comment_item13 = Column(Text, nullable=True)
    comment_item14 = Column(Text, nullable=True)
    comment_item15 = Column(Text, nullable=True)
    comment_item16 = Column(Text, nullable=True)
    comment_item17 = Column(Text, nullable=True)
    comment_item18 = Column(Text, nullable=True)
    comment_item19 = Column(Text, nullable=True)
    comment_item20 = Column(Text, nullable=True)
    comment_item21 = Column(Text, nullable=True)
    comment_item22 = Column(Text, nullable=True)
    comment_item23 = Column(Text, nullable=True)
    comment_item24 = Column(Text, nullable=True)
    comment_item25 = Column(Text, nullable=True)
    comment_item26 = Column(Text, nullable=True)
    comment_item27a = Column(Text, nullable=True)
    comment_item27b = Column(Text, nullable=True)
    comment_item28 = Column(Text, nullable=True)
    comment_item29 = Column(Text, nullable=True)

# Create the database tables.
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def calculate_score_and_validate(form_data: dict) -> Tuple[List[str], Optional[int], Optional[float]]:
    errors = []
    # Extract project information.
    project_name = form_data.get("project_name", "N/A")
    battalion = form_data.get("battalion", "N/A")
    oic_name = form_data.get("oic_name", "N/A")
    aoic_name = form_data.get("aoic_name", "N/A")
    start_date = form_data.get("start_date", "")
    planned_start = form_data.get("planned_start", "")
    planned_completion = form_data.get("planned_completion", "")
    actual_completion = form_data.get("actual_completion", "")

    # For radio/select items, we expect positive values for normal selections
    # and negative values to indicate N/A. Comments are required only when N/A is selected.
    item1 = parse_int(form_data.get("item1", "0"))
    comment_item1 = form_data.get("comment_item1", "").strip()
    if item1 < 0 and not comment_item1:
        errors.append("Item 1 requires a comment when N/A is selected.")

    item2 = parse_int(form_data.get("item2", "0"))
    comment_item2 = form_data.get("comment_item2", "").strip()
    if item2 < 0 and not comment_item2:
        errors.append("Item 2 requires a comment when N/A is selected.")

    item3 = parse_int(form_data.get("item3", "0"))
    comment_item3 = form_data.get("comment_item3", "").strip()
    if item3 < 0 and not comment_item3:
        errors.append("Item 3 requires a comment when N/A is selected.")

    # Item 4: if using calculation, use the calculated score; otherwise use the provided option.
    item4_option = form_data.get("item4_option", "calc")
    if item4_option == "calc":
        item4 = parse_int(form_data.get("item4_score", "16"))
    else:
        item4 = parse_int(item4_option)
    comment_item4 = form_data.get("comment_item4", "").strip()
    # For item 4, a comment is required if the score is not perfect (16)
    if item4 != 16 and not comment_item4:
        errors.append("Item 4 requires a comment if score is not perfect.")

    item5 = parse_int(form_data.get("item5", "0"))
    comment_item5 = form_data.get("comment_item5", "").strip()
    if item5 < 0 and not comment_item5:
        errors.append("Item 5 requires a comment when N/A is selected.")

    item6 = parse_int(form_data.get("item6", "0"))
    comment_item6 = form_data.get("comment_item6", "").strip()
    if item6 < 0 and not comment_item6:
        errors.append("Item 6 requires a comment when N/A is selected.")

    item78 = parse_int(form_data.get("item78", "0"))
    comment_item78 = form_data.get("comment_item78", "").strip()
    if item78 < 0 and not comment_item78:
        errors.append("Items 7 & 8 require a comment when N/A is selected.")

    item9 = parse_int(form_data.get("item9", "0"))
    comment_item9 = form_data.get("comment_item9", "").strip()
    if item9 < 0 and not comment_item9:
        errors.append("Item 9 requires a comment when N/A is selected.")

    item10 = parse_int(form_data.get("item10", "0"))
    comment_item10 = form_data.get("comment_item10", "").strip()
    if item10 < 0 and not comment_item10:
        errors.append("Item 10 requires a comment when N/A is selected.")

    item11 = parse_int(form_data.get("item11", "0"))
    comment_item11 = form_data.get("comment_item11", "").strip()
    if item11 < 0 and not comment_item11:
        errors.append("Item 11 requires a comment when N/A is selected.")

    item12 = parse_int(form_data.get("item12", "0"))
    comment_item12 = form_data.get("comment_item12", "").strip()
    if item12 < 0 and not comment_item12:
        errors.append("Item 12 requires a comment when N/A is selected.")

    item13 = parse_int(form_data.get("item13", "0"))
    comment_item13 = form_data.get("comment_item13", "").strip()
    if item13 < 0 and not comment_item13:
        errors.append("Item 13 requires a comment when N/A is selected.")

    item14 = parse_int(form_data.get("item14", "0"))
    comment_item14 = form_data.get("comment_item14", "").strip()
    if item14 < 0 and not comment_item14:
        errors.append("Item 14 requires a comment when N/A is selected.")

    item15 = parse_int(form_data.get("item15", "0"))
    comment_item15 = form_data.get("comment_item15", "").strip()
    if item15 < 0 and not comment_item15:
        errors.append("Item 15 requires a comment when N/A is selected.")

    item16 = parse_int(form_data.get("item16", "0"))
    comment_item16 = form_data.get("comment_item16", "").strip()
    if item16 < 0 and not comment_item16:
        errors.append("Item 16 requires a comment when N/A is selected.")

    item17 = parse_int(form_data.get("item17", "0"))
    comment_item17 = form_data.get("comment_item17", "").strip()
    if item17 < 0 and not comment_item17:
        errors.append("Item 17 requires a comment when N/A is selected.")

    item18 = parse_int(form_data.get("item18", "0"))
    comment_item18 = form_data.get("comment_item18", "").strip()
    if item18 < 0 and not comment_item18:
        errors.append("Item 18 requires a comment when N/A is selected.")

    item19 = parse_int(form_data.get("item19", "0"))
    comment_item19 = form_data.get("comment_item19", "").strip()
    if item19 < 0 and not comment_item19:
        errors.append("Item 19 requires a comment when N/A is selected.")

    item20 = parse_int(form_data.get("item20", "0"))
    comment_item20 = form_data.get("comment_item20", "").strip()
    if item20 < 0 and not comment_item20:
        errors.append("Item 20 requires a comment when N/A is selected.")

    item21 = parse_int(form_data.get("item21", "0"))
    comment_item21 = form_data.get("comment_item21", "").strip()
    if item21 < 0 and not comment_item21:
        errors.append("Item 21 requires a comment when N/A is selected.")

    item22 = parse_int(form_data.get("item22", "0"))
    comment_item22 = form_data.get("comment_item22", "").strip()
    if item22 < 0 and not comment_item22:
        errors.append("Item 22 requires a comment when N/A is selected.")

    item23 = parse_int(form_data.get("item23", "0"))
    comment_item23 = form_data.get("comment_item23", "").strip()
    if item23 < 0 and not comment_item23:
        errors.append("Item 23 requires a comment when N/A is selected.")

    item24 = parse_int(form_data.get("item24", "0"))
    deduction24 = parse_int(form_data.get("deduction24", "0"))
    comment_item24 = form_data.get("comment_item24", "").strip()
    # For Item 24, if a deduction is applied (i.e. deduction > 0) then comment is required.
    if deduction24 > 0 and not comment_item24:
        errors.append("Item 24 requires a comment when a deduction is applied.")

    item25 = parse_int(form_data.get("item25", "0"))
    comment_item25 = form_data.get("comment_item25", "").strip()
    if item25 < 0 and not comment_item25:
        errors.append("Item 25 requires a comment when N/A is selected.")

    item26 = parse_int(form_data.get("item26", "0"))
    comment_item26 = form_data.get("comment_item26", "").strip()
    if item26 < 0 and not comment_item26:
        errors.append("Item 26 requires a comment when N/A is selected.")

    item27a = parse_int(form_data.get("item27a", "0"))
    comment_item27a = form_data.get("comment_item27a", "").strip()
    if item27a < 0 and not comment_item27a:
        errors.append("Item 27a requires a comment when N/A is selected.")

    item27b = parse_int(form_data.get("item27b", "0"))
    comment_item27b = form_data.get("comment_item27b", "").strip()
    if item27b < 0 and not comment_item27b:
        errors.append("Item 27b requires a comment when N/A is selected.")

    item28 = parse_int(form_data.get("item28_option", "0"))
    deduction28 = parse_int(form_data.get("deduction28", "0"))
    comment_item28 = form_data.get("comment_item28", "").strip()
    if deduction28 > 0 and not comment_item28:
        errors.append("Item 28 requires a comment when a deduction is applied.")

    item29 = parse_int(form_data.get("item29_option", "0"))
    deduction29 = parse_int(form_data.get("deduction29", "0"))
    comment_item29 = form_data.get("comment_item29", "").strip()
    if deduction29 > 0 and not comment_item29:
        errors.append("Item 29 requires a comment when a deduction is applied.")

    if errors:
        return errors, None, None

    # Calculate total score (manual deductions for items 24, 28, and 29 are applied)
    total_score = (
        item1 + item2 + item3 + item4 + item5 + item6 + item78 +
        item9 + item10 + item11 + item12 + item13 + item14 + item15 +
        item16 + item17 + item18 + item19 + item20 + item21 +
        item22 + item23 + (item24 - deduction24) + item25 + item26 +
        item27a + item27b + (item28 - deduction28) + (item29 - deduction29)
    )
    final_percentage = round(total_score / 171 * 100, 1)
    return [], total_score, final_percentage

@app.get("/", respo
