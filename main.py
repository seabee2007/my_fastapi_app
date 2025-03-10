from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
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

def calculate_score_and_validate(form_data: dict) -> Tuple[List[str], Optional[int], Optional[float]]:
    errors = []
    # Extract project information
    project_name = form_data.get("project_name", "N/A")
    battalion = form_data.get("battalion", "N/A")
    oic_name = form_data.get("oic_name", "N/A")
    aoic_name = form_data.get("aoic_name", "N/A")
    start_date = form_data.get("start_date", "")
    planned_start = form_data.get("planned_start", "")
    planned_completion = form_data.get("planned_completion", "")
    actual_completion = form_data.get("actual_completion", "")

    def parse_int(value, default=0):
        try:
            return int(value)
        except:
            return default

    # Parse numeric values and corresponding comments.
    item1 = parse_int(form_data.get("item1", "0"))
    comment_item1 = form_data.get("comment_item1", "").strip()
    if item1 != 2 and not comment_item1:
        errors.append("Item 1 requires a comment if not perfect.")

    item2 = parse_int(form_data.get("item2", "0"))
    comment_item2 = form_data.get("comment_item2", "").strip()
    if item2 != 2 and not comment_item2:
        errors.append("Item 2 requires a comment if not perfect.")

    item3 = parse_int(form_data.get("item3", "0"))
    comment_item3 = form_data.get("comment_item3", "").strip()
    if item3 != 4 and not comment_item3:
        errors.append("Item 3 requires a comment if not perfect.")

    # For Item 4, check if calculation option was used.
    item4_option = form_data.get("item4_option", "calc")
    if item4_option == "calc":
        item4 = parse_int(form_data.get("item4_score", "16"))
    else:
        item4 = parse_int(item4_option)
    comment_item4 = form_data.get("comment_item4", "").strip()
    if item4 != 16 and not comment_item4:
        errors.append("Item 4 requires a comment if score is not perfect.")

    item5 = parse_int(form_data.get("item5", "0"))
    comment_item5 = form_data.get("comment_item5", "").strip()
    if item5 != 2 and not comment_item5:
        errors.append("Item 5 requires a comment if not perfect.")

    item6 = parse_int(form_data.get("item6", "0"))
    comment_item6 = form_data.get("comment_item6", "").strip()
    if item6 != 4 and not comment_item6:
        errors.append("Item 6 requires a comment if score is not perfect.")

    item78 = parse_int(form_data.get("item78", "0"))
    comment_item78 = form_data.get("comment_item78", "").strip()
    if item78 != 4 and not comment_item78:
        errors.append("Items 7 & 8 require a comment if score is not perfect.")

    item9 = parse_int(form_data.get("item9", "0"))
    comment_item9 = form_data.get("comment_item9", "").strip()
    if item9 != 4 and not comment_item9:
        errors.append("Item 9 requires a comment if score is not perfect.")

    item10 = parse_int(form_data.get("item10", "0"))
    comment_item10 = form_data.get("comment_item10", "").strip()
    if item10 != 4 and not comment_item10:
        errors.append("Item 10 requires a comment if score is not perfect.")

    item11 = parse_int(form_data.get("item11", "0"))
    comment_item11 = form_data.get("comment_item11", "").strip()
    if item11 != 4 and not comment_item11:
        errors.append("Item 11 requires a comment if not perfect.")

    item12 = parse_int(form_data.get("item12", "0"))
    comment_item12 = form_data.get("comment_item12", "").strip()
    if item12 != 4 and not comment_item12:
        errors.append("Item 12 requires a comment if score is not perfect.")

    item13 = parse_int(form_data.get("item13", "0"))
    comment_item13 = form_data.get("comment_item13", "").strip()
    if item13 != 4 and not comment_item13:
        errors.append("Item 13 requires a comment if score is not perfect.")

    item14 = parse_int(form_data.get("item14", "0"))
    comment_item14 = form_data.get("comment_item14", "").strip()
    if item14 != 10 and not comment_item14:
        errors.append("Item 14 requires a comment if score is not perfect.")

    item15 = parse_int(form_data.get("item15", "0"))
    comment_item15 = form_data.get("comment_item15", "").strip()
    if item15 != 2 and not comment_item15:
        errors.append("Item 15 requires a comment if not perfect.")

    item16 = parse_int(form_data.get("item16", "0"))
    comment_item16 = form_data.get("comment_item16", "").strip()
    if item16 != 10 and not comment_item16:
        errors.append("Item 16 requires a comment if score is not perfect.")

    item17 = parse_int(form_data.get("item17", "0"))
    comment_item17 = form_data.get("comment_item17", "").strip()
    if item17 != 2 and not comment_item17:
        errors.append("Item 17 requires a comment if not perfect.")

    item18 = parse_int(form_data.get("item18", "0"))
    comment_item18 = form_data.get("comment_item18", "").strip()
    if item18 != 2 and not comment_item18:
        errors.append("Item 18 requires a comment if not perfect.")

    item19 = parse_int(form_data.get("item19", "0"))
    comment_item19 = form_data.get("comment_item19", "").strip()
    if item19 != 5 and not comment_item19:
        errors.append("Item 19 requires a comment if score is not perfect.")

    item20 = parse_int(form_data.get("item20", "0"))
    comment_item20 = form_data.get("comment_item20", "").strip()
    if item20 != 6 and not comment_item20:
        errors.append("Item 20 requires a comment if score is not perfect.")

    item21 = parse_int(form_data.get("item21", "0"))
    comment_item21 = form_data.get("comment_item21", "").strip()
    if item21 != 6 and not comment_item21:
        errors.append("Item 21 requires a comment if score is not perfect.")

    item22 = parse_int(form_data.get("item22", "0"))
    comment_item22 = form_data.get("comment_item22", "").strip()
    if item22 != 12 and not comment_item22:
        errors.append("Item 22 requires a comment if score is not perfect.")

    item23 = parse_int(form_data.get("item23", "0"))
    comment_item23 = form_data.get("comment_item23", "").strip()
    if item23 != 5 and not comment_item23:
        errors.append("Item 23 requires a comment if score is not perfect.")

    item24 = parse_int(form_data.get("item24", "0"))
    deduction24 = parse_int(form_data.get("deduction24", "0"))
    comment_item24 = form_data.get("comment_item24", "").strip()
    if deduction24 != 0 and not comment_item24:
        errors.append("Item 24 requires a comment if a deduction is applied.")

    item25 = parse_int(form_data.get("item25", "0"))
    comment_item25 = form_data.get("comment_item25", "").strip()
    if item25 != 8 and not comment_item25:
        errors.append("Item 25 requires a comment if score is not perfect.")

    item26 = parse_int(form_data.get("item26", "0"))
    comment_item26 = form_data.get("comment_item26", "").strip()
    if item26 != 4 and not comment_item26:
        errors.append("Item 26 requires a comment if score is not perfect.")

    item27a = parse_int(form_data.get("item27a", "0"))
    comment_item27a = form_data.get("comment_item27a", "").strip()
    if item27a != 10 and not comment_item27a:
        errors.append("Item 27a requires a comment if score is not perfect.")

    item27b = parse_int(form_data.get("item27b", "0"))
    comment_item27b = form_data.get("comment_item27b", "").strip()
    if item27b != 5 and not comment_item27b:
        errors.append("Item 27b requires a comment if score is not perfect.")

    item28 = parse_int(form_data.get("item28_option", "0"))
    deduction28 = parse_int(form_data.get("deduction28", "0"))
    comment_item28 = form_data.get("comment_item28", "").strip()
    if deduction28 != 0 and not comment_item28:
        errors.append("Item 28 requires a comment if a deduction is applied.")

    item29 = parse_int(form_data.get("item29_option", "0"))
    deduction29 = parse_int(form_data.get("deduction29", "0"))
    comment_item29 = form_data.get("comment_item29", "").strip()
    if deduction29 != 0 and not comment_item29:
        errors.append("Item 29 requires a comment if a deduction is applied.")

    if errors:
        return errors, None, None

    # Calculate total score by summing all items (including manual deductions)
    total_score = (
        item1 + item2 + item3 + item4 + item5 + item6 + item78 +
        item9 + item10 + item11 + item12 + item13 + item14 + item15 +
        item16 + item17 + item18 + item19 + item20 + item21 +
        item22 + item23 + (item24 - deduction24) + item25 + item26 +
        item27a + item27b + (item28 - deduction28) + (item29 - deduction29)
    )
    final_percentage = round(total_score / 171 * 100, 1)
    return [], total_score, final_percentage

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit_assessment", response_class=HTMLResponse)
async def submit_assessment(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    data_dict = dict(form_data)
    errors, final_score, final_percentage = calculate_score_and_validate(data_dict)

    if errors:
        return templates.TemplateResponse("index.html", {"request": request, "errors": errors, "form_data": data_dict})
    else:
        assessment = Assessment(
            project_name=data_dict.get("project_name", "N/A"),
            battalion=data_dict.get("battalion", "N/A"),
            oic_name=data_dict.get("oic_name", "N/A"),
            aoic_name=data_dict.get("aoic_name", "N/A"),
            start_date=data_dict.get("start_date", ""),
            planned_start=data_dict.get("planned_start", ""),
            planned_completion=data_dict.get("planned_completion", ""),
            actual_completion=data_dict.get("actual_completion", ""),
            final_score=final_score,
            final_percentage=final_percentage,
            comment_item1=data_dict.get("comment_item1", "").strip(),
            comment_item2=data_dict.get("comment_item2", "").strip(),
            comment_item3=data_dict.get("comment_item3", "").strip(),
            comment_item4=data_dict.get("comment_item4", "").strip(),
            comment_item5=data_dict.get("comment_item5", "").strip(),
            comment_item6=data_dict.get("comment_item6", "").strip(),
            comment_item78=data_dict.get("comment_item78", "").strip(),
            comment_item9=data_dict.get("comment_item9", "").strip(),
            comment_item10=data_dict.get("comment_item10", "").strip(),
            comment_item11=data_dict.get("comment_item11", "").strip(),
            comment_item12=data_dict.get("comment_item12", "").strip(),
            comment_item13=data_dict.get("comment_item13", "").strip(),
            comment_item14=data_dict.get("comment_item14", "").strip(),
            comment_item15=data_dict.get("comment_item15", "").strip(),
            comment_item16=data_dict.get("comment_item16", "").strip(),
            comment_item17=data_dict.get("comment_item17", "").strip(),
            comment_item18=data_dict.get("comment_item18", "").strip(),
            comment_item19=data_dict.get("comment_item19", "").strip(),
            comment_item20=data_dict.get("comment_item20", "").strip(),
            comment_item21=data_dict.get("comment_item21", "").strip(),
            comment_item22=data_dict.get("comment_item22", "").strip(),
            comment_item23=data_dict.get("comment_item23", "").strip(),
            comment_item24=data_dict.get("comment_item24", "").strip(),
            comment_item25=data_dict.get("comment_item25", "").strip(),
            comment_item26=data_dict.get("comment_item26", "").strip(),
            comment_item27a=data_dict.get("comment_item27a", "").strip(),
            comment_item27b=data_dict.get("comment_item27b", "").strip(),
            comment_item28=data_dict.get("comment_item28", "").strip(),
            comment_item29=data_dict.get("comment_item29", "").strip()
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return templates.TemplateResponse("report.html", {"request": request, "assessment": assessment})
