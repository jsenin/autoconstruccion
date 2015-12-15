import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from autoconstruccion import db
from autoconstruccion.models import Project, User, Skill, SkillLevel


def create_mock_project_by_id(id):
    project = Project()
    project.id = id
    project.name = "Project"
    project.description = "Description"
    project.start_date = datetime.date(2015, 12, 12)
    project.end_date = datetime.date(2015, 12, 12)
    project.location = "here"
    project.contact_phone = "666666666"
    project.image = None
    db.session.add(project)


def create_mock_user_by_id(id):
    user = User()
    user.id = id
    user.full_name = "UserName"
    user.email = "username@user.com"
    user.phone_number = "666666666"
    db.session.add(user)


def create_mock_skill_by_id(id):
    skill = Skill()
    skill.id = id
    skill.name = "skill"
    skill.description = "description"
    skill.image = None
    db.session.add(skill)


def test_all_of_PK_must_unique(request_ctx):
    create_mock_project_by_id(1)
    create_mock_user_by_id(1)
    create_mock_skill_by_id(1)

    create_mock_project_by_id(2)
    create_mock_user_by_id(2)
    create_mock_skill_by_id(2)

    db.session.execute('pragma foreign_keys=on')
    db.session.flush()

    skill_level_id_1 = SkillLevel()
    skill_level_id_1.project_id = 1
    skill_level_id_1.user_id = 1
    skill_level_id_1.skill_id = 1
    db.session.add(skill_level_id_1)

    db.session.flush()

    skill_level_id_2 = SkillLevel()
    skill_level_id_2.project_id = 2
    skill_level_id_2.user_id = 2
    skill_level_id_2.skill_id = 2
    db.session.add(skill_level_id_2)
    db.session.commit()


def test_throw_exception_when_commit_id_non_existent(request_ctx):
    db.session.execute('pragma foreign_keys=on')

    skill_level = SkillLevel()
    skill_level.project_id = 1
    skill_level.user_id = 1
    skill_level.skill_id = 1

    db.session.add(skill_level)
    with pytest.raises(IntegrityError):
        db.session.commit()
