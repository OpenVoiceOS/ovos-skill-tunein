#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-tunein.jarbasai=skill_tunein:TuneInSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-tunein',
    version='0.0.1',
    description='ovos tunein skill plugin',
    url='https://github.com/JarbasSkills/skill-tunein',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_tunein": ""},
    package_data={'skill_tunein': ['locale/*', 'ui/*']},
    packages=['skill_tunein'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a7", "tunein~=0.0.1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
