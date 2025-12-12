from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .controller.controller import router
app = FastAPI()


# ⬅️ اصلاح نهایی: هندلر سفارشی برای خطای 422 که آن را به 400 تبدیل می‌کند
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]

    field_name = first_error['loc'][-1] if first_error['loc'] else 'request body'

    message = f"Invalid input for '{field_name}': {first_error['msg']}"

    return JSONResponse(
        # ⬅️ تغییر مهم: استفاده از 400 BAD_REQUEST مطابق با AC
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "failure",
            "message": message,
            "data": " "
        },
    )


app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to URL Shortener API"}
