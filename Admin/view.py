from DataBase.models import UserAdmin, ProfileAdmin, OtpAdmin, UserTypeAdmin, TeacherCategoryAdmin, TeacherAdmin, \
    CourseAdmin, EnrolledCoursesAdmin, ReviewAdmin, VariantAdmin, VariantItemAdmin
from app import app as admin_app

# Modellarni admin panelga qo'shish
admin_app.register_model(UserAdmin)
admin_app.register_model(ProfileAdmin)
admin_app.register_model(OtpAdmin)
admin_app.register_model(UserTypeAdmin)
admin_app.register_model(TeacherCategoryAdmin)
admin_app.register_model(TeacherAdmin)
admin_app.register_model(CourseAdmin)
admin_app.register_model(EnrolledCoursesAdmin)
admin_app.register_model(ReviewAdmin)
admin_app.register_model(VariantAdmin)
admin_app.register_model(VariantItemAdmin)

# FastAPI-Admin ni FastAPI ilovasiga ulash
admin_app.mount("/admin", admin_app)
