from abc import ABC, abstractmethod
from typing import List

class BaseRenderer(ABC):
    @abstractmethod
    def render_education(eductation_list: List[str]) -> str:
        pass
    
    @abstractmethod
    def render_experience(experience_list: List[str]) -> str:
        pass
    
    @abstractmethod
    def render_projects(project_list: List[str]) -> str:
        pass
    
    @abstractmethod
    def render_skills(project_list: List[str]) -> str:
        pass