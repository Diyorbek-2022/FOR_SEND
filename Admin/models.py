from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from fastapi import Depends

from DataBase.database import engine
from DataBase.models import User
from app import app


# Avvalgi kodda aniqlangan modellar va sozlamalarni import qilish


# Dependency: Sessiyani olish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin panelni FastAPI ga ulash
admin = Admin(app, engine)

# Har bir model uchun ModelView yaratish
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username, User.otp_id]
    column_searchable_list = [User.email, User.username]
    column_sortable_list = [User.id, User.email]
    page_size = 10

class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.user_id, Profile.country, Profile.username, Profile.type_id, Profile.enrolled_id]
    column_searchable_list = [Profile.username, Profile.country]
    column_sortable_list = [Profile.id, Profile.user_id]
    page_size = 10

class OtpAdmin(ModelView, model=Otp):
    column_list = [Otp.id, Otp.code, Otp.created_at]
    column_searchable_list = [Otp.code]
    column_sortable_list = [Otp.id, Otp.created_at]
    page_size = 10

class UserTypeAdmin(ModelView, model=UserType):
    column_list = [UserType.id, UserType.type]
    column_searchable_list = [UserType.type]
    column_sortable_list = [UserType.id]
    page_size = 10

class TeacherCategoryAdmin(ModelView, model=TeacherCategory):
    column_list = [TeacherCategory.id, TeacherCategory.name]
    column_searchable_list = [TeacherCategory.name]
    column_sortable_list = [TeacherCategory.id]
    page_size = 10

class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id, Teacher.category_id]
    column_sortable_list = [Teacher.id]
    page_size = 10

class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.teacher_id, Course.type, Course.price, Course.level, Course.language, Course.published, Course.featured, Course.slug]
    column_searchable_list = [Course.type, Course.level, Course.language, Course.slug]
    column_sortable_list = [Course.id, Course.price]
    page_size = 10

class EnrolledCoursesAdmin(ModelView, model=EnrolledCourses):
    column_list = [EnrolledCourses.id, EnrolledCourses.user_id, EnrolledCourses.course_id]
    column_sortable_list = [EnrolledCourses.id]
    page_size = 10

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.user_id, Review.course_id, Review.rating, Review.active]
    column_searchable_list = [Review.text]
    column_sortable_list = [Review.id, Review.rating]
    page_size = 10

class VariantAdmin(ModelView, model=Variant):
    column_list = [Variant.id, Variant.course_id, Variant.title, Variant.preview, Variant.date]
    column_searchable_list = [Variant.title]
    column_sortable_list = [Variant.id, Variant.date]
    page_size = 10

class VariantItemAdmin(ModelView, model=VariantItem):
    column_list = [VariantItem.id, VariantItem.variant_id, VariantItem.title, VariantItem.preview, VariantItem.date]
    column_searchable_list = [VariantItem.title]
    column_sortable_list = [VariantItem.id, VariantItem.date]
    page_size = 10

# Modellarni admin panelga qo'shish
admin.add_view(UserAdmin)
admin.add_view(ProfileAdmin)
admin.add_view(OtpAdmin)
admin.add_view(UserTypeAdmin)
admin.add_view(TeacherCategoryAdmin)
admin.add_view(TeacherAdmin)
admin.add_view(CourseAdmin)
admin.add_view(EnrolledCoursesAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(VariantAdmin)
admin.add_view(VariantItemAdmin)