from datetime import date, timedelta
from fastapi import APIRouter
from src.api.dependencies import SessionDep
from src.database import Base, engine
from src.models.tasks import CategoryModel, DayModel, TaskModel

router = APIRouter()

@router.post("/setup_database")
async def setup_database(session: SessionDep):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await init_summer_days(session)
    return {"ok": True}

@router.post("/init_database")
async def init_database(db: SessionDep):
    await setup_database(db)
    categories = {
        "Programming": CategoryModel(title="Programming"),
        "Gym": CategoryModel(title="Gym"),
        "English": CategoryModel(title="English"),
        "Food": CategoryModel(title="Eat"),
        "Working": CategoryModel(title="Working")
    }

    for cat in categories.values():
        db.add(cat)
    await db.commit()

    tasks_data = {
        16: [
            ("few tasks on leetcode (1.5 hours)", 1),
            ("2 hours", 2),
            ("20 min", 3),
            ("Rice + 1 chicken + 1 turkey leg (2 times). Protein", 4)
        ],
        17: [
            ("few tasks on leetcode (> 1 hours)", 1),
            ("2+ hours", 2),
            ("1 hour", 3),
            ("Rice + 1 chicken + 1 turkey leg (2 times). 200 gramm milk. Protein", 4)
        ],
        18: [
            ("3 hours", 1),
            ("2 hours + pool", 2),
            ("40 minutes", 3),
            ("Rice + 1 chicken + 1 turkey leg. Potato with 1 chicken kyivs. Protein", 4)
        ],
        19: [
            ("1.5 - 2 hours", 1),
            ("1.5 hours", 2),
            ("McDonalds. Rice + 1 chicken + 1 turkey leg. Potato + chicken kyiv. Protein", 4)
        ],
        20: [
            ("40 minutes (1 task)", 1),
            ("swom in the sea", 2),
            ("20 minutes", 3),
            ("bolonyiesa and pizza. protein", 4)
        ],
        21: [
            ("1 hour 10 minutes", 1),
            ("horizontal bars", 2),
            ("few minutes", 3),
            ("Potato with 1 chicken kyivs. Beens (415 hr), avocado and 2 sandwiches with peenutes butter, and Protein. bolonyiesa", 4)
        ],
        22: [
            ("1 hour", 3),
            ("fish + pasta. chicken kyivs and 2 eggs with potato. 2 Peanut butter sandwiches.", 4),
            ("7 hours (1 hour brake)", 5)
        ],
        23: [
            ("Chicken (2x)", 4),
            ("7 hours (1 hour brake)", 5)
        ],
        24: [
            ("Chicken. beef and potato. Pasta an chicken.", 4),
            ("6 hours (1 hour brake)", 5)
        ],
        25: [
            ("1 hour", 1),
            ("1.4 hours", 2),
            ("1.5 hour", 3),
            ("chicken. Tuna (185hr). 5 sandwiches and protein", 4)
        ],
        26: [
            ("1.4 hours", 2),
            ("Protein and else", 4)
        ],
        27: [
            ("> 1 hour", 1)
        ],
        28: [
            ("Chicken + rice + egg and banana. Turkey and rice.", 4),
            ("11.1", 5)
        ],
        29: [
            ("Картошку с мясом и банан. Рис с индюком.", 4),
            ("9.1", 5)
        ],
        30: [
            ("more than 3 hours", 1),
            ("1.5 hours", 2),
            ("Protein. Rice and turkey. Dumplings. One apple", 4)
        ],
        31: [
            ("mb 2 hours", 1),
            ("1 hour 30-40 minutes", 2),
            ("25 minutes", 3),
            ("Tuna (185 gr). 2 chicken thighs with potatos. Protein. 2 chiken thighs with pasta and 1 egg. ", 4)
        ],
        32: [
            ("Chicken Pasta (43 hr protein) + cherry tomatoes. 2 chicken thighs with pasta and 1 egg.", 4)
        ],
        33: [
            ("Tuna (95 hr). Beef and potato. Kiwi. 2 chicken thighs with pasta and 1 egg.", 4)
        ],
        34: [
            ("3 hours", 1),
            ("2 hours", 2),
            ("2 chicken thighs with pasta and 1 egg and salad. Tuna (95 hr, 16 protein) + avocado. Protein. 3 chicken thighs with pasta and 1 egg.", 4)
        ],
        35: [
            ("4 hours", 1),
            ("3 chicken thighs with buckwheat. Avocado. Protein.", 4)
        ]
    }

    for day_id, tasks in tasks_data.items():
        for desc, cat_id in tasks:
            task = TaskModel(
                    description=desc,
                    completed=True,
                    day_id=day_id,
                    category_id=cat_id
                )
            db.add(task)
    
    await db.commit()
    return {"ok": True}


async def init_summer_days(session: SessionDep):
    SUMMER_START = date(2025, 6, 1)
    SUMMER_END = date(2025, 8, 31)
    current_day = SUMMER_START
    while current_day <= SUMMER_END:
        if not await session.get(DayModel, current_day):
            session.add(DayModel(date=current_day))
        current_day += timedelta(days=1)
    await session.commit()