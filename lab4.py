import pytest
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages import ContactPage

class TestContactForm:
    """Тесты для контактной формы"""
    
    @pytest.fixture
    def setup(self):
        """Фикстура для настройки браузера"""
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        
        # Получаем абсолютный путь к HTML-файлу
        file_path = os.path.abspath('form.html')
        driver.get(f"file:///D:/4%20курс/тестирование/лаб4/lab4/form.html")
        
        self.contact_page = ContactPage(driver)
        
        yield self.contact_page
        
        driver.quit()
    
    # ПОЗИТИВНЫЙ ТЕСТ
    def test_successful_form_submission(self, setup):
        """Позитивный тест: успешная отправка формы с валидными данными"""
        contact_page = setup
        
        # Данные для заполнения формы
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'email': 'ivan.petrov@example.com',
            'phone': '+7 (999) 123-45-67',
            'subject': 'technical',
            'message': 'Добрый день! У меня возникла проблема с использованием вашего продукта. Можете помочь?',
            'agreement': True
        }
        
        # Заполняем форму
        contact_page.fill_form(form_data)
        
        # Отправляем форму
        contact_page.submit_form()
        
        # Проверяем успешную отправку
        assert contact_page.is_success_message_displayed(), "Сообщение об успехе не отображается"
        
        print("✓ Позитивный тест пройден: форма успешно отправлена")
    
    # НЕГАТИВНЫЕ ТЕСТЫ
    def test_empty_required_field(self, setup):
        """Негативный тест: попытка отправки формы с пустым обязательным полем"""
        contact_page = setup
        
        # Заполняем все поля кроме одного обязательного
        form_data = {
            'first_name': 'Иван',  # Заполнено
            'last_name': '',       # ПУСТОЕ ОБЯЗАТЕЛЬНОЕ ПОЛЕ
            'email': 'ivan@example.com',
            'subject': 'sales',
            'message': 'Тестовое сообщение длиной более 10 символов',
            'agreement': True
        }
        
        contact_page.fill_form(form_data)
        contact_page.submit_form()
        
        # Проверяем сообщение об ошибке
        error_text = contact_page.get_error_message('last_name')
        assert error_text == "Поле \"Фамилия\" обязательно для заполнения", f"Неверное сообщение об ошибке: {error_text}"
        
        # Проверяем, что у поля есть стиль ошибки
        assert contact_page.is_field_has_error('last_name'), "Поле не имеет стиля ошибки"
        
        # Проверяем, что сообщение об успехе НЕ отображается
        assert not contact_page.is_success_message_displayed(), "Сообщение об успехе отображается, хотя не должно"
        
        print("✓ Негативный тест пройден: корректная валидация пустого обязательного поля")
    
    def test_invalid_email_format(self, setup):
        """Негативный тест: неверный формат email"""
        contact_page = setup
        
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'email': 'invalid-email',  # НЕВЕРНЫЙ ФОРМАТ
            'subject': 'technical',
            'message': 'Тестовое сообщение для проверки валидации email',
            'agreement': True
        }
        
        contact_page.fill_form(form_data)
        contact_page.submit_form()
        
        error_text = contact_page.get_error_message('email')
        assert error_text == "Введите корректный email адрес", f"Неверное сообщение об ошибке: {error_text}"
        assert contact_page.is_field_has_error('email')
        
        print("✓ Негативный тест пройден: корректная валидация email")
    
    def test_short_message(self, setup):
        """Негативный тест: сообщение слишком короткое"""
        contact_page = setup
        
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'email': 'ivan@example.com',
            'subject': 'other',
            'message': 'Коротко',  # СЛИШКОМ КОРОТКОЕ СООБЩЕНИЕ
            'agreement': True
        }
        
        contact_page.fill_form(form_data)
        contact_page.submit_form()
        
        error_text = contact_page.get_error_message('message')
        assert error_text == "Сообщение должно содержать от 10 до 500 символов", f"Неверное сообщение об ошибке: {error_text}"
        assert contact_page.is_field_has_error('message')
        
        print("✓ Негативный тест пройден: корректная валидация длины сообщения")
    
    def test_without_agreement(self, setup):
        """Негативный тест: отправка без согласия"""
        contact_page = setup
        
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'email': 'ivan@example.com',
            'subject': 'partnership',
            'message': 'Достаточно длинное сообщение для тестирования',
            'agreement': False  # БЕЗ СОГЛАСИЯ
        }
        
        contact_page.fill_form(form_data)
        contact_page.submit_form()
        
        error_text = contact_page.get_error_message('agreement')
        assert error_text == "Необходимо ваше согласие", f"Неверное сообщение об ошибке: {error_text}"
        
        print("✓ Негативный тест пройден: корректная валидация согласия")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])