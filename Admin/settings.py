import redis

from app import app

redis_client = redis.Redis(host="localhost", port=6379, db=0)

# FastAPI-Admin sozlamalari
@app.on_event("startup")
async def startup():
    await admin_app.configure(
        logo_url="https://fastapi-admin.github.io/logo.png",
        template_folders=["templates"],
        providers=[],
        redis=redis_client,
        admin_path="/admin",
        title="FastAPI Admin",
        login_path="/admin/login",
        logout_path="/admin/logout",
    )

# Admin uchun modellar
class UserAdmin(ModelAdmin, model=User):
    list_display = ["id", "email", "username", "otp_id"]
    list_filter = ["email", "username"]
    search_fields = ["email", "username"]

class ProfileAdmin(ModelAdmin, model=Profile):
    list_display = ["id", "user_id", "country", "username", "type_id", "enrolled_id"]
    list_filter = ["country"]
    search_fields = ["username", "country"]

class OtpAdmin(ModelAdmin, model=Otp):
    list_display = ["id", "code", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["code"]

class UserTypeAdmin(ModelAdmin, model=UserType):
    list_display = ["id", "type"]
    search_fields = ["type"]

class TeacherCategoryAdmin(ModelAdmin, model=TeacherCategory):
    list_display = ["id", "name"]
    search_fields = ["name"]

class TeacherAdmin(ModelAdmin, model=Teacher):
    list_display = ["id", "category_id"]

class CourseAdmin(ModelAdmin, model=Course):
    list_display = ["id", "teacher_id", "type", "price", "level", "language", "published", "featured", "slug"]
    list_filter = ["type", "level", "language", "published", "featured"]
    search_fields = ["slug"]

class EnrolledCoursesAdmin(ModelAdmin, model=EnrolledCourses):
    list_display = ["id", "user_id", "course_id"]

class ReviewAdmin(ModelAdmin, model=Review):
    list_display = ["id", "user_id", "course_id", "rating", "active", "date"]
    list_filter = ["active", "date"]
    search_fields = ["text"]

class VariantAdmin(ModelAdmin, model=Variant):
    list_display = ["id", "course_id", "title", "preview", "date"]
    list_filter = ["preview", "date"]
    search_fields = ["title"]

class VariantItemAdmin(ModelAdmin, model=VariantItem):
    list_display = ["id", "variant_id", "title", "preview", "date"]
    list_filter = ["preview", "date"]
    search_fields = ["title"]