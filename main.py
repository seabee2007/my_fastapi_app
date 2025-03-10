from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from fastapi.staticfiles import StaticFiles

# Database configuration using SQLite.
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Assessment model.
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
    # NEW: Adjusted maximum total possible for applicable items.
    adjusted_total_max = Column(Integer, nullable=True)
    errors = Column(Text, nullable=True)
    signature_oic = Column(Text, nullable=True)
    signature_ncr = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Comments for items 1–29
    comment_item1 = Column(Text, nullable=True)
    comment_item2 = Column(Text, nullable=True)
    comment_item3 = Column(Text, nullable=True)
    comment_item4 = Column(Text, nullable=True)
    comment_item5 = Column(Text, nullable=True)
    comment_item6 = Column(Text, nullable=True)
    comment_item78 = Column(Text, nullable=True)  # Items 7 & 8 combined
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
    except Exception:
        return default

# Perfect scores for each item.
PERFECT_SCORES = {
    "item1": 2,
    "item2": 2,
    "item3": 4,
    "item4": 16,
    "item5": 2,
    "item6": 4,
    "item78": 4,
    "item9": 4,
    "item10": 4,
    "item11": 4,
    "item12": 4,
    "item13": 4,
    "item14": 10,
    "item15": 2,
    "item16": 10,
    "item17": 2,
    "item18": 2,
    "item19": 5,
    "item20": 6,
    "item21": 6,
    "item22": 12,
    "item23": 5,
    "item24": 20,
    "item25": 8,
    "item26": 4,
    "item27a": 10,
    "item27b": 5,
    "item28": 5,
    "item29": 5,
}

# Updated validation function.
# For every item, if a score is provided (submitted >= 0) and it is less than the perfect score,
# then a comment is required. (N/A items, with negative score, still require a comment.)
# Also, every item must have a submitted value.
def calculate_score_and_validate(form_data: dict):
    errors = []
    score_sum = 0
    max_possible = 0

    def process_item(key, comment_key, perfect):
        nonlocal score_sum, max_possible
        # Get the submitted value; assume it is always present (if not, default to empty string)
        raw = form_data.get(key, "")
        if raw == "":
            errors.append(f"Item {key[-1]} is required.")
            return
        submitted = parse_int(raw)
        comment = form_data.get(comment_key, "").strip()
        if submitted < 0:
            # N/A case
            if not comment:
                errors.append(f"Item {key[-1]} requires a comment when N/A is selected.")
        else:
            # If not perfect, a comment is required.
            if submitted != perfect and not comment:
                errors.append(f"Item {key[-1]} requires a comment if score is less than maximum ({perfect}).")
            score_sum += submitted
            max_possible += perfect

    # Process items without deductions.
    for key in ["item1", "item2", "item3", "item5", "item6", "item78", "item9",
                "item10", "item11", "item12", "item13", "item14", "item15", "item16",
                "item17", "item18", "item19", "item20", "item21", "item22", "item23",
                "item25", "item26", "item27a", "item27b"]:
        process_item(key, f"comment_{key}", PERFECT_SCORES[key])

    # Process Item 4 separately.
    item4_option = form_data.get("item4_option", "calc")
    if item4_option == "calc":
        raw4 = form_data.get("item4_score", "")
        if raw4 == "":
            errors.append("Item 4 score is required.")
            item4_val = 0
        else:
            item4_val = parse_int(raw4)
    else:
        item4_val = parse_int(item4_option)
    comment_item4 = form_data.get("comment_item4", "").strip()
    if item4_option != "calc" and item4_val < 0:
        if not comment_item4:
            errors.append("Item 4 requires a comment when N/A is selected.")
    else:
        if item4_val != PERFECT_SCORES["item4"] and not comment_item4:
            errors.append("Item 4 requires a comment if the score is not perfect (16).")
        if item4_val >= 0:
            score_sum += item4_val
            max_possible += PERFECT_SCORES["item4"]

    # Process items with manual deductions (24, 28, 29).
    def process_deducted_item(key, deduction_key, comment_key, perfect):
        nonlocal score_sum, max_possible
        raw = form_data.get(key, "")
        if raw == "":
            errors.append(f"Item {key[-1]} is required.")
            return
        submitted = parse_int(raw)
        deduction = parse_int(form_data.get(deduction_key, "0"))
        comment = form_data.get(comment_key, "").strip()
        if submitted < 0:
            if not comment:
                errors.append(f"Item {key[-1]} requires a comment when N/A is selected.")
        else:
            computed = submitted - deduction
            if computed != perfect and not comment:
                errors.append(f"Item {key[-1]} requires a comment if score after deduction is less than maximum ({perfect}).")
            score_sum += computed
            max_possible += perfect

    process_deducted_item("item24", "deduction24", "comment_item24", PERFECT_SCORES["item24"])
    process_deducted_item("item28_option", "deduction28", "comment_item28", PERFECT_SCORES["item28"])
    process_deducted_item("item29_option", "deduction29", "comment_item29", PERFECT_SCORES["item29"])

    if errors:
        return errors, None, None, None

    final_percentage = round(score_sum / max_possible * 100, 1) if max_possible > 0 else 0
    return [], score_sum, final_percentage, max_possible

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "form_data": {}})

@app.post("/submit_assessment", response_class=HTMLResponse)
async def submit_assessment(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    data_dict = dict(form_data)
    errors, final_score, final_percentage, max_possible = calculate_score_and_validate(data_dict)
    if errors:
        return templates.TemplateResponse("index.html", {"request": request, "errors": errors, "form_data": data_dict})
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
        adjusted_total_max=max_possible,
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
