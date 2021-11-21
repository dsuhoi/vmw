from app import db

class Articles(db.Model):
    #__tablename__ == 'articles'
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    chapter = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False, default='Текст')

    def __repr__(self):
	    return "<{}:{}>".format(self.id,  self.title)
