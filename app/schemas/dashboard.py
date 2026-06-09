from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_students: int

    low_balance_students: int

    out_of_sessions_students: int

    today_classes: int

    monthly_revenue: float