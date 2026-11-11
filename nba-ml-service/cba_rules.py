def check_salary_legality(outgoing_salary: float, incoming_salary: float, team_tax_status: str = "NON_TAXPAYER"):
    if team_tax_status == "SECOND_APRON":
        is_legal = incoming_salary <= outgoing_salary
        max_allowed = outgoing_salary
        reason = "Second Apron: Cannot take back more salary than sent out (100% rule)."

    elif team_tax_status == "FIRST_APRON":
        is_legal = incoming_salary <= outgoing_salary
        max_allowed = outgoing_salary
        reason = "First Apron: Dollar-for-dollar matching only."

    else:
        if outgoing_salary <= 9.1:
            max_allowed = (outgoing_salary * 2.0) + 0.25
        elif outgoing_salary <= 35.2:
            max_allowed = outgoing_salary + 9.1
        else: 
            max_allowed = (outgoing_salary * 1.25) + 0.25

        is_legal = incoming_salary <= max_allowed
        reason = f"Standard Tier: Allowed up to ${max_allowed:.2f}M incoming salary."

    return {
        "is_legal": is_legal,
        "outgoing_salary": outgoing_salary,
        "incoming_salary": incoming_salary,
        "max_allowed_incoming": round(max_allowed, 2),
        "rule_note": reason
    }