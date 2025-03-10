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
    except Exception:
        return default

# Define the perfect score for each item.
# For items with deductions, the perfect score remains constant.
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

# This function validates the form and computes two sums:
# - score_sum: the sum of points earned for applicable items.
# - max_possible: the sum of perfect scores for applicable items.
# For each item, if the submitted value is negative (i.e. N/A), then that item is
# not applicable and its perfect score is removed from the maximum.
# (Item 4 uses a calculated value if the "calc" option is used.)
def calculate_score_and_validate(form_data: dict):
    errors = []
    score_sum = 0
    max_possible = 0

    # Helper to process an individual item.
    # key: the key name for the form value.
    # perfect: perfect score for the item.
    # comment_key: key for the comment field.
    # extra: an optional function to modify the submitted value (e.g. for deductions)
    def process_item(key, perfect, comment_key, extra=lambda x: x):
        nonlocal score_sum, max_possible
        submitted = parse_int(form_data.get(key, "0"))
        comment = form_data.get(comment_key, "").strip()
        # If the item is marked as N/A (negative), require a comment and do not add to denominator.
        if submitted < 0:
            if not comment:
                errors.append(f"{key.capitalize()} requires a comment when N/A is selected.")
            # Do not add to score_sum or max_possible.
        else:
            val = extra(submitted)
            score_sum += val
            max_possible += perfect

    # Process items 1,2,3,5,6,7/8 (item78),9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27a,27b.
    for key, perfect in {
        "item1": PERFECT_SCORES["item1"],
        "item2": PERFECT_SCORES["item2"],
        "item3": PERFECT_SCORES["item3"],
        "item5": PERFECT_SCORES["item5"],
        "item6": PERFECT_SCORES["item6"],
        "item78": PERFECT_SCORES["item78"],
        "item9": PERFECT_SCORES["item9"],
        "item10": PERFECT_SCORES["item10"],
        "item11": PERFECT_SCORES["item11"],
        "item12": PERFECT_SCORES["item12"],
        "item13": PERFECT_SCORES["item13"],
        "item14": PERFECT_SCORES["item14"],
        "item15": PERFECT_SCORES["item15"],
        "item16": PERFECT_SCORES["item16"],
        "item17": PERFECT_SCORES["item17"],
        "item18": PERFECT_SCORES["item18"],
        "item19": PERFECT_SCORES["item19"],
        "item20": PERFECT_SCORES["item20"],
        "item21": PERFECT_SCORES["item21"],
        "item22": PERFECT_SCORES["item22"],
        "item23": PERFECT_SCORES["item23"],
        "item25": PERFECT_SCORES["item25"],
        "item26": PERFECT_SCORES["item26"],
        "item27a": PERFECT_SCORES["item27a"],
        "item27b": PERFECT_SCORES["item27b"],
    }.items():
        process_item(key, perfect, f"comment_{key}")

    # Process Item 4 separately (it can use a calculation or an N/A option)
    item4_option = form_data.get("item4_option", "calc")
    if item4_option == "calc":
        item4_val = parse_int(form_data.get("item4_score", "16"))
    else:
        item4_val = parse_int(item4_option)
    comment_item4 = form_data.get("comment_item4", "").strip()
    if item4_option != "calc" and item4_val < 0:
        if not comment_item4:
            errors.append("Item 4 requires a comment when N/A is selected.")
    else:
        # Even if using calculation, if score is less than perfect, require comment.
        if item4_val != PERFECT_SCORES["item4"] and not comment_item4:
            errors.append("Item 4 requires a comment if the score is not perfect.")
        # Only count item 4 if it is applicable (i.e. non-negative)
        if item4_val >= 0:
            score_sum += item4_val
            max_possible += PERFECT_SCORES["item4"]

    # Process items with manual deductions: 24, 28, 29.
    # For each, if the select value is negative then the item is N/A.
    # Otherwise, subtract the deduction from the submitted value.
    def process_deducted_item(key, deduction_key, perfect, comment_key):
        nonlocal score_sum, max_possible
        submitted = parse_int(form_data.get(key, "0"))
        deduction = parse_int(form_data.get(deduction_key, "0"))
        comment = form_data.get(comment_key, "").strip()
        if submitted < 0:
            if not comment:
                errors.append(f"{key.capitalize()} requires a comment when N/A is selected.")
        else:
            val = submitted - deduction
            score_sum += val
            max_possible += perfect

    process_deducted_item("item24", "deduction24", PERFECT_SCORES["item24"], "comment_item24")
    process_deducted_item("item28_option", "deduction28", PERFECT_SCORES["item28"], "comment_item28")
    process_deducted_item("item29_option", "deduction29", PERFECT_SCORES["item29"], "comment_item29")

    if errors:
        return errors, None, None

    # If no items were applicable, set maximum to 0 to avoid division by zero.
    final_percentage = round(score_sum / max_possible * 100, 1) if max_possible > 0 else 0
    return [], score_sum, final_percentage

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
