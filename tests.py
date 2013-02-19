from sqlalchemy import Column, Integer, Unicode, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_sluggable import Sluggable


class TestCase(object):
    def setup_method(self, method):
        self.engine = create_engine('sqlite:///:memory:')
        self.Model = declarative_base()

        self.Post = self.create_post_model(**self.slug_options)
        self.Model.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def teardown_method(self, method):
        self.session.close_all()
        self.Model.metadata.drop_all(self.engine)
        self.engine.dispose()

    def create_post_model(self, **slug_options):
        class Post(self.Model, Sluggable):
            __tablename__ = 'posts'

            id = Column(Integer, primary_key=True)
            title = Column(Unicode(255), nullable=False)

            __sluggable__ = slug_options

            def __init__(self, title):
                self.title = title

        return Post


class TestSluggableAlwaysUpdate(TestCase):

    slug_options = {
        'populate_from': 'title',
        'always_update': True
    }

    def test_creates_slug_on_insert(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()
        assert post.slug == u'hello-world'

    def test_ensures_the_slug_is_unique_on_insert(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()

        post2 = self.Post(u'Hello World!')
        self.session.add(post2)
        self.session.commit()

        assert post2.slug == u'hello-world-2'

    def test_updates_slug_on_update(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()

        post.title = u'Hello again!'
        self.session.commit()
        assert post.slug == u'hello-again'

    def test_doesnt_increment_slug_index_on_update_if_slug_doesnt_change(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()

        post.title = u'hello world'
        self.session.commit()
        assert post.slug == u'hello-world'


class TestSluggableNoUpdate(TestCase):

    slug_options = {
        'populate_from': 'title',
        'always_update': False
    }

    def test_doesnt_update_slug_on_update(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()

        post.title = u'Hello again!'
        self.session.commit()
        assert post.slug == u'hello-world'


class TestSluggableCustomSeparator(TestCase):

    slug_options = {
        'populate_from': 'title',
        'separator': '_'
    }

    def test_creates_slug_with_custom_separator_on_insert(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()
        assert post.slug == u'hello_world'

    def test_uses_custom_separator_to_separate_postfix_number(self):
        post = self.Post(u'Hello World!')
        self.session.add(post)
        self.session.commit()

        post2 = self.Post(u'Hello World!')
        self.session.add(post2)
        self.session.commit()

        assert post2.slug == u'hello_world_2'
