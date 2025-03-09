from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Tuple, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Request
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


app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




# Create the database tables.
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_score_and_validate(form_data: dict) -> Tuple[List[str], Optional[int], Optional[float]]:
    errors = []
    # Extract project info.
    project_name = form_data.get("project_name", "N/A")
    battalion = form_data.get("battalion", "N/A")
    oic_name = form_data.get("oic_name", "N/A")
    aoic_name = form_data.get("aoic_name", "N/A")
    start_date = form_data.get("start_date", "")
    planned_start = form_data.get("planned_start", "")
    planned_completion = form_data.get("planned_completion", "")
    actual_completion = form_data.get("actual_completion", "")

    def parse_int_or_str(val):
        try:
            return int(val)
        except:
            return val

    # Parse form items and their comments.
    item1 = form_data.get("item1", "No")
    comment_item1 = form_data.get("comment_item1", "").strip()

    item2 = form_data.get("item2", "No")
    comment_item2 = form_data.get("comment_item2", "").strip()

    item3 = form_data.get("item3", "No")
    comment_item3 = form_data.get("comment_item3", "").strip()

    item4_score_str = form_data.get("item4_score", "16")
    item4_score = parse_int_or_str(item4_score_str)
    comment_item4 = form_data.get("comment_item4", "").strip()

    item5 = form_data.get("item5", "No")
    comment_item5 = form_data.get("comment_item5", "").strip()

    item6_str = form_data.get("item6", "4")
    item6 = parse_int_or_str(item6_str)
    comment_item6 = form_data.get("comment_item6", "").strip()

    item78_str = form_data.get("item78", "4")
    item78 = parse_int_or_str(item78_str)
    comment_item78 = form_data.get("comment_item78", "").strip()

    item9_str = form_data.get("item9", "4")
    item9 = parse_int_or_str(item9_str)
    comment_item9 = form_data.get("comment_item9", "").strip()

    item10 = form_data.get("item10", "N/A")
    comment_item10 = form_data.get("comment_item10", "").strip()

    item11 = form_data.get("item11", "No")
    comment_item11 = form_data.get("comment_item11", "").strip()

    item12_str = form_data.get("item12", "4")
    item12 = parse_int_or_str(item12_str)
    comment_item12 = form_data.get("comment_item12", "").strip()

    item13_str = form_data.get("item13", "4")
    item13 = parse_int_or_str(item13_str)
    comment_item13 = form_data.get("comment_item13", "").strip()

    item14_str = form_data.get("item14", "10")
    item14 = parse_int_or_str(item14_str)
    comment_item14 = form_data.get("comment_item14", "").strip()

    item15 = form_data.get("item15", "No")
    comment_item15 = form_data.get("comment_item15", "").strip()

    item16_str = form_data.get("item16", "10")
    item16 = parse_int_or_str(item16_str)
    comment_item16 = form_data.get("comment_item16", "").strip()

    item17 = form_data.get("item17", "No")
    comment_item17 = form_data.get("comment_item17", "").strip()

    item18 = form_data.get("item18", "No")
    comment_item18 = form_data.get("comment_item18", "").strip()

    item19_str = form_data.get("item19", "5")
    item19 = parse_int_or_str(item19_str)
    comment_item19 = form_data.get("comment_item19", "").strip()

    item20_str = form_data.get("item20", "6")
    item20 = parse_int_or_str(item20_str)
    comment_item20 = form_data.get("comment_item20", "").strip()

    item21_str = form_data.get("item21", "6")
    item21 = parse_int_or_str(item21_str)
    comment_item21 = form_data.get("comment_item21", "").strip()

    item22_str = form_data.get("item22", "12")
    item22 = parse_int_or_str(item22_str)
    comment_item22 = form_data.get("comment_item22", "").strip()

    item23_str = form_data.get("item23", "5")
    item23 = parse_int_or_str(item23_str)
    comment_item23 = form_data.get("comment_item23", "").strip()

    item24_str = form_data.get("item24", "20")
    deduction24_str = form_data.get("deduction24", "0")
    item24 = parse_int_or_str(item24_str)
    deduction24 = parse_int_or_str(deduction24_str)
    comment_item24 = form_data.get("comment_item24", "").strip()

    item25_str = form_data.get("item25", "8")
    item25 = parse_int_or_str(item25_str)
    comment_item25 = form_data.get("comment_item25", "").strip()

    item26_str = form_data.get("item26", "4")
    item26 = parse_int_or_str(item26_str)
    comment_item26 = form_data.get("comment_item26", "").strip()

    item27a_str = form_data.get("item27a", "10")
    item27a = parse_int_or_str(item27a_str)
    comment_item27a = form_data.get("comment_item27a", "").strip()

    item27b_str = form_data.get("item27b", "5")
    item27b = parse_int_or_str(item27b_str)
    comment_item27b = form_data.get("comment_item27b", "").strip()

    deduction28_str = form_data.get("deduction28", "0")
    deduction28 = parse_int_or_str(deduction28_str)
    comment_item28 = form_data.get("comment_item28", "").strip()

    deduction29_str = form_data.get("deduction29", "0")
    deduction29 = parse_int_or_str(deduction29_str)
    comment_item29 = form_data.get("comment_item29", "").strip()

    # Validate that a comment is provided when an item is not perfect.
    if item1 != "Yes" and not comment_item1:
        errors.append("Item 1 requires a comment if not perfect.")
    if item2 != "Yes" and not comment_item2:
        errors.append("Item 2 requires a comment if not perfect.")
    if item3 != "Yes" and not comment_item3:
        errors.append("Item 3 requires a comment if not perfect.")
    if item4_score != 16 and not comment_item4:
        errors.append("Item 4 requires a comment if score is not 16.")
    if item5 != "Yes" and not comment_item5:
        errors.append("Item 5 requires a comment if not perfect.")
    if item6 != 4 and not comment_item6:
        errors.append("Item 6 requires a comment if score is not 4.")
    if item78 != 4 and not comment_item78:
        errors.append("Items 7 & 8 require a comment if score is not 4.")
    if item9 != 4 and not comment_item9:
        errors.append("Item 9 requires a comment if score is not 4.")
    if item10 not in ["N/A", "4"] and not comment_item10:
        errors.append("Item 10 requires a comment if score is not perfect.")
    if item11 != "Yes" and not comment_item11:
        errors.append("Item 11 requires a comment if not perfect.")
    if item12 != 4 and not comment_item12:
        errors.append("Item 12 requires a comment if score is not 4.")
    if item13 != 4 and not comment_item13:
        errors.append("Item 13 requires a comment if score is not 4.")
    if item14 != 10 and not comment_item14:
        errors.append("Item 14 requires a comment if score is not 10.")
    if item15 != "Yes" and not comment_item15:
        errors.append("Item 15 requires a comment if not perfect.")
    if item16 != 10 and not comment_item16:
        errors.append("Item 16 requires a comment if score is not 10.")
    if item17 != "Yes" and not comment_item17:
        errors.append("Item 17 requires a comment if not perfect.")
    if item18 != "Yes" and not comment_item18:
        errors.append("Item 18 requires a comment if not perfect.")
    if item19 != 5 and not comment_item19:
        errors.append("Item 19 requires a comment if score is not 5.")
    if item20 != 6 and not comment_item20:
        errors.append("Item 20 requires a comment if score is not 6.")
    if item21 != 6 and not comment_item21:
        errors.append("Item 21 requires a comment if score is not 6.")
    if item22 != 12 and not comment_item22:
        errors.append("Item 22 requires a comment if score is not 12.")
    if item23 != 5 and not comment_item23:
        errors.append("Item 23 requires a comment if score is not 5.")
    if deduction24 != 0 and not comment_item24:
        errors.append("Item 24 requires a comment if a deduction is applied.")
    if item25 != 8 and not comment_item25:
        errors.append("Item 25 requires a comment if score is not 8.")
    if item26 != 4 and not comment_item26:
        errors.append("Item 26 requires a comment if score is not 4.")
    if item27a != 10 and not comment_item27a:
        errors.append("Item 27a requires a comment if score is not 10.")
    if item27b != 5 and not comment_item27b:
        errors.append("Item 27b requires a comment if score is not 5.")
    if deduction28 != 0 and not comment_item28:
        errors.append("Item 28 requires a comment if a deduction is applied.")
    if deduction29 != 0 and not comment_item29:
        errors.append("Item 29 requires a comment if a deduction is applied.")

    if errors:
        return errors, None, None

    # Calculate numeric scores.
    score1   = 2 if item1  == "Yes" else 0
    score2   = 2 if item2  == "Yes" else 0
    score3   = 4 if item3  == "Yes" else 0
    score4   = item4_score
    score5   = 2 if item5  == "Yes" else 0
    score6   = item6
    score7_8 = item78
    score9   = item9
    score10  = 4 if item10 == "4" else 0
    score11  = 4 if item11 == "Yes" else 0
    score12  = item12
    score13  = item13
    score14  = item14
    score15  = 2 if item15 == "Yes" else 0
    score16  = item16
    score17  = 2 if item17 == "Yes" else 0
    score18  = 2 if item18 == "Yes" else 0
    score19  = item19
    score20  = item20
    score21  = item21
    score22  = item22
    score23  = item23
    score24  = (20 - deduction24)
    score25  = item25
    score26  = item26
    score27a = item27a
    score27b = item27b
    score28  = (5 - deduction28)
    score29  = (5 - deduction29)

    total_score = (score1 + score2 + score3 + score4 + score5 +
                   score6 + score7_8 + score9 + score10 + score11 +
                   score12 + score13 + score14 + score15 + score16 +
                   score17 + score18 + score19 + score20 + score21 +
                   score22 + score23 + score24 + score25 + score26 +
                   score27a + score27b + score28 + score29)

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
            comment_item1 = data_dict.get("comment_item1", "").strip(),
            comment_item2 = data_dict.get("comment_item2", "").strip(),
            comment_item3 = data_dict.get("comment_item3", "").strip(),
            comment_item4 = data_dict.get("comment_item4", "").strip(),
            comment_item5 = data_dict.get("comment_item5", "").strip(),
            comment_item6 = data_dict.get("comment_item6", "").strip(),
            comment_item78 = data_dict.get("comment_item78", "").strip(),
            comment_item9 = data_dict.get("comment_item9", "").strip(),
            comment_item10 = data_dict.get("comment_item10", "").strip(),
            comment_item11 = data_dict.get("comment_item11", "").strip(),
            comment_item12 = data_dict.get("comment_item12", "").strip(),
            comment_item13 = data_dict.get("comment_item13", "").strip(),
            comment_item14 = data_dict.get("comment_item14", "").strip(),
            comment_item15 = data_dict.get("comment_item15", "").strip(),
            comment_item16 = data_dict.get("comment_item16", "").strip(),
            comment_item17 = data_dict.get("comment_item17", "").strip(),
            comment_item18 = data_dict.get("comment_item18", "").strip(),
            comment_item19 = data_dict.get("comment_item19", "").strip(),
            comment_item20 = data_dict.get("comment_item20", "").strip(),
            comment_item21 = data_dict.get("comment_item21", "").strip(),
            comment_item22 = data_dict.get("comment_item22", "").strip(),
            comment_item23 = data_dict.get("comment_item23", "").strip(),
            comment_item24 = data_dict.get("comment_item24", "").strip(),
            comment_item25 = data_dict.get("comment_item25", "").strip(),
            comment_item26 = data_dict.get("comment_item26", "").strip(),
            comment_item27a = data_dict.get("comment_item27a", "").strip(),
            comment_item27b = data_dict.get("comment_item27b", "").strip(),
            comment_item28 = data_dict.get("comment_item28", "").strip(),
            comment_item29 = data_dict.get("comment_item29", "").strip(),
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return RedirectResponse(url=f"/report/{assessment.id}", status_code=303)

@app.post("/save_signatures/{assessment_id}")
async def save_signatures(assessment_id: int,
                          oic_signature: Optional[str] = Form(None),
                          ncr_signature: Optional[str] = Form(None),
                          db: Session = Depends(get_db)):
    assessment = db.query(Assessment).get(assessment_id)
    if not assessment:
        return HTMLResponse("Assessment not found", status_code=404)
    assessment.signature_oic = oic_signature
    assessment.signature_ncr = ncr_signature
    db.commit()
    return RedirectResponse(url=f"/report/{assessment.id}", status_code=303)

@app.get("/report/{assessment_id}", response_class=HTMLResponse)
def print_report(assessment_id: int, request: Request, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).get(assessment_id)
    if not assessment:
        return HTMLResponse("Assessment not found", status_code=404)
    return templates.TemplateResponse("report.html", {"request": request, "assessment": assessment})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
