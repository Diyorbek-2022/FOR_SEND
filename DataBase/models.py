from fastapi import FastAPI, Depends
from fastapi_admin.app import app as admin_app
from fastapi_admin.contrib.sqlmodel import ModelAdmin
from fastapi_admin.depends import get_current_admin
from fastapi_admin.resources import Link
from fastapi_admin.template import templates
from fastapi_admin.utils import pwd_context
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import redis.asyncio as redis

# FastAPI ilovasini yaratish
app = FastAPI()

# SQLite ma'lumotlar bazasi uchun ulanish (PostgreSQL uchun o'zgartirish mumkin)
DATABASE_URL = "sqlite:///caksizbilimbackend.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis ulanishi
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Modellar (avvalgi so'rovlaringizdan olingan)
class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)

    profiles = relationship("Profile", back_populates="type")

    def __str__(self):
        return self.type

class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="otp")

    def __str__(self):
        return self.code

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    otp_id = Column(Integer, ForeignKey("otps.id"), nullable=False)
    refresh_token = Column(String(1000), nullable=True)
    username = Column(String(100), unique=True, nullable=False)

    otp = relationship("Otp", back_populates="user")
    profile = relationship("Profile", uselist=False, back_populates="user")
    reviews = relationship("Review", back_populates="user")
    enrolled_courses = relationship("EnrolledCourses", back_populates="user")

    @classmethod
    def create(cls, session, email, otp_id, refresh_token=None, username=None, **profile_kwargs):
        email_username = email.split("@")[0]
        user_instance = cls(
            email=email,
            otp_id=otp_id,
            refresh_token=refresh_token,
            username=username if username else email_username
        )
        user_instance.profile = Profile(
            user=user_instance,
            username=user_instance.username,
            **profile_kwargs
        )
        session.add(user_instance)
        return user_instance

    def __str__(self):
        return self.email

class TeacherCategory(Base):
    __tablename__ = "teacher_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    teachers = relationship("Teacher", back_populates="category")

    def __str__(self):
        return self.name

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("teacher_categories.id"), nullable=False)

    category = relationship("TeacherCategory", back_populates="teachers")
    courses = relationship("Course", back_populates="teacher")

    def __str__(self):
        return f"Teacher {self.id}"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    type = Column(String(10), nullable=False)
    intro_video = Column(String, nullable=True)
    image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    level = Column(String(10), nullable=False)
    language = Column(String(10), nullable=False)
    published = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    slug = Column(String(100), unique=True, nullable=False)

    teacher = relationship("Teacher", back_populates="courses")
    enrolled_courses = relationship("EnrolledCourses", back_populates="course")
    variants = relationship("Variant", back_populates="course")
    reviews = relationship("Review", back_populates="course")

    def __str__(self):
        return self.slug

class EnrolledCourses(Base):
    __tablename__ = "enrolled_courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    user = relationship("User", back_populates="enrolled_courses")
    course = relationship("Course", back_populates="enrolled_courses")
    profiles = relationship("Profile", back_populates="enrolled")

    def __str__(self):
        return f"{self.user.username} - {self.course.slug}"

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    country = Column(String(100), unique=True, nullable=False)
    about = Column(Text, nullable=True)
    full_name = Column(String(100), nullable=True)
    username = Column(String(100), unique=True, nullable=True)
    image = Column(String, nullable=True)
    type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)
    enrolled_id = Column(Integer, ForeignKey("enrolled_courses.id"), nullable=False)

    user = relationship("User", back_populates="profile")
    type = relationship("UserType", back_populates="profiles")
    enrolled = relationship("EnrolledCourses", back_populates="profiles")

    def __str__(self):
        return self.username

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    text = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    reply = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    reply_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="reviews")
    course = relationship("Course", back_populates="reviews")

    def __str__(self):
        return f"{self.user.username} - {self.rating}"

class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)
    preview = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="variants")
    variant_items = relationship("VariantItem", back_populates="variant")

    def __str__(self):
        return self.title

class VariantItem(Base):
    __tablename__ = "variant_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)
    preview = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)

    variant = relationship("Variant", back_populates="variant_items")

    def __str__(self):
        return self.title

# Ma'lumotlar bazasini yaratish
Base.metadata.create_all(bind=engine)

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



# Serverni ishga tushirish
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)