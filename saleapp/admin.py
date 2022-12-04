from saleapp import admin, db, app
from saleapp.models import Hoa_don, \
    Ve_may_bay, Nguoi_dung, Tuyen_bay, May_bay, San_bay, Chuyen_bay, Ghe, San_bay_trung_gian
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Hoa_don,db.session))
admin.add_view(ModelView(Ve_may_bay, db.session))
admin.add_view(ModelView(Tuyen_bay, db.session))
admin.add_view(ModelView(May_bay, db.session))
admin.add_view(ModelView(San_bay, db.session))
admin.add_view(ModelView(Chuyen_bay, db.session))
admin.add_view(ModelView(Ghe, db.session))
admin.add_view(ModelView(San_bay_trung_gian, db.session))