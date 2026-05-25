import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers import retrieve_phone_code


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # ============================
    # LOCALIZADORES - ROTA
    # ============================

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    suggest_item = (By.CSS_SELECTOR, "li.suggest-item")
    overlay = (By.CLASS_NAME, "overlay")

    # ============================
    # LOCALIZADORES - TÁXI
    # ============================

    CALL_A_TAXI_BUTTON = (By.XPATH, '//button[text()="Chamar um táxi"]')
    comfort_button = (By.XPATH, "//div[contains(@class,'tcard')][.//div[contains(text(),'Comfort')]]")

    # ============================
    # LOCALIZADORES - TELEFONE
    # ============================

    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    next_phone_button = (By.XPATH, "//button[contains(text(),'Próximo')]")

    # ============================
    # LOCALIZADORES - PAGAMENTO
    # ============================

    payment_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[contains(text(),'Adicionar cartão')]")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//div[@class='card-code']//input")
    card_add_confirm = (By.XPATH, "//button[contains(text(),'Adicionar') or contains(text(),'Salvar')]")

    close_card_modal_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    # ============================
    # LOCALIZADORES - COMENTÁRIO
    # ============================

    MESSAGE_FOR_DRIVER_FIELD = (By.ID, 'comment')
    #comment_field = (By.XPATH, "//*[@id='comment']")
    #comment_field = (By.XPATH,  "//*[@id='comment']")


    # ============================
    # LOCALIZADORES - EXTRAS
    # ============================

    #comment_input = (By.XPATH, "//input[@id='comment' and @name='comment']")

    extras_button = (By.XPATH, "//button[contains(.,'pedido')]")

    comfort_button = (By.XPATH, "//div[contains(@class,'tcard') and .//div[contains(text(),'Comfort')]]")

    BLANKET_AND_HANDKERCHIEFS_OPTION_DIV = (
        By.XPATH,
        "//div[contains(text(), 'Cobertor e lençóis')]/following-sibling::div[1]/div"
    )

    BLANKET_AND_HANDKERCHIEFS_OPTION_INPUT = (
        By.XPATH,
        "//div[contains(text(), 'Cobertor e lençóis')]/following-sibling::div[1]/div/input"
    )

    ICECREAM_PLUS = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Sorvete']/following::div[@class='counter-plus'][1]"
    )

    ICECREAM_VALUE = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Sorvete']/following::div[@class='counter-value'][1]"
    )

    # ============================
    # LOCALIZADORES - SMS
    # ============================

    sms_input = (By.ID, "code")
    sms_confirm_button = (By.XPATH, "//button[contains(text(),'Confirmar')]")
    phone_modal = (By.CLASS_NAME, "modal")

    # ============================
... (237 linhas)

message.txt
12 KB
Camila — Ontem às 00:10
MAIN.PY :
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--remote-allow-origins=*")

        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def open_page(self):
        self.driver.get(data.URBAN_ROUTES_URL + "/?lng=pt")
        return UrbanRoutesPage(self.driver)

    # ============================================================
    # 1️⃣ Definir rota
    # ============================================================
    def test_set_route(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        assert data.ADDRESS_FROM.lower() in page.get_from_field_text().lower()
        assert data.ADDRESS_TO.lower() in page.get_to_field_text().lower()

    # ============================================================
    # 2️⃣ Selecionar Comfort
    # ============================================================
    def test_select_comfort_rate(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_taxi()
        time.sleep(2)

        page.select_comfort()

        assert page.is_comfort_selected()

    # ============================================================
    # 3️⃣ Telefone
    # ============================================================
    def test_fill_phone_number(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        page.click_taxi()
        time.sleep(2)

        page.open_phone_modal()
        page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(1)

        page.click_next_phone()
        time.sleep(2)

        # ⭐ Capturar o SMS automaticamente
        sms_code = retrieve_phone_code(page.driver)

        # ⭐ Preencher o SMS
        page.fill_sms_code(sms_code)

        # ⭐ Confirmar o SMS
        page.confirm_sms()

        # ⭐ Esperar o modal sumir
        page.wait_phone_modal_disappear()

        # ✅ Assert: número salvo aparece na tela
        assert data.PHONE_NUMBER in page.driver.page_source

    # ============================================================
    # 4️⃣ Cartão de crédito
    # ============================================================
    def test_add_credit_card(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        page.click_taxi()
... (136 linhas)

message.txt
8 KB
voce precisa desses 3 ai
o que faz os teste rodar é o que estar no MAIN
pronto esta ai , so conseguir te mandar agora . amanha vou focar no 9 . o 8 vou deixar em pausa
﻿
Camila
camih_sts
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers import retrieve_phone_code


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # ============================
    # LOCALIZADORES - ROTA
    # ============================

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    suggest_item = (By.CSS_SELECTOR, "li.suggest-item")
    overlay = (By.CLASS_NAME, "overlay")

    # ============================
    # LOCALIZADORES - TÁXI
    # ============================

    CALL_A_TAXI_BUTTON = (By.XPATH, '//button[text()="Chamar um táxi"]')
    comfort_button = (By.XPATH, "//div[contains(@class,'tcard')][.//div[contains(text(),'Comfort')]]")

    # ============================
    # LOCALIZADORES - TELEFONE
    # ============================

    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    next_phone_button = (By.XPATH, "//button[contains(text(),'Próximo')]")

    # ============================
    # LOCALIZADORES - PAGAMENTO
    # ============================

    payment_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[contains(text(),'Adicionar cartão')]")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//div[@class='card-code']//input")
    card_add_confirm = (By.XPATH, "//button[contains(text(),'Adicionar') or contains(text(),'Salvar')]")

    close_card_modal_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    # ============================
    # LOCALIZADORES - COMENTÁRIO
    # ============================

    MESSAGE_FOR_DRIVER_FIELD = (By.ID, 'comment')
    #comment_field = (By.XPATH, "//*[@id='comment']")
    #comment_field = (By.XPATH,  "//*[@id='comment']")


    # ============================
    # LOCALIZADORES - EXTRAS
    # ============================

    #comment_input = (By.XPATH, "//input[@id='comment' and @name='comment']")

    extras_button = (By.XPATH, "//button[contains(.,'pedido')]")

    comfort_button = (By.XPATH, "//div[contains(@class,'tcard') and .//div[contains(text(),'Comfort')]]")

    BLANKET_AND_HANDKERCHIEFS_OPTION_DIV = (
        By.XPATH,
        "//div[contains(text(), 'Cobertor e lençóis')]/following-sibling::div[1]/div"
    )

    BLANKET_AND_HANDKERCHIEFS_OPTION_INPUT = (
        By.XPATH,
        "//div[contains(text(), 'Cobertor e lençóis')]/following-sibling::div[1]/div/input"
    )

    ICECREAM_PLUS = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Sorvete']/following::div[@class='counter-plus'][1]"
    )

    ICECREAM_VALUE = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Sorvete']/following::div[@class='counter-value'][1]"
    )

    # ============================
    # LOCALIZADORES - SMS
    # ============================

    sms_input = (By.ID, "code")
    sms_confirm_button = (By.XPATH, "//button[contains(text(),'Confirmar')]")
    phone_modal = (By.CLASS_NAME, "modal")

    # ============================
    # UTILITÁRIOS
    # ============================

    def _find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

    def wait_overlay_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.overlay))
        except:
            pass

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def _press_tab(self):
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

        # ============================
        # MÉTODOS - ROTA
        # ============================

    def set_route(self, from_address, to_address):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        self._type(self.from_field, from_address)
        self._type(self.to_field, to_address)

    def get_from_field_text(self):
        return self._get_value(self.from_field)

    def get_to_field_text(self):
        return self._get_value(self.to_field)

        # ============================
        # MÉTODOS - TÁXI
        # ============================

    def click_taxi(self):
        self._click(self.CALL_A_TAXI_BUTTON)

    def select_comfort(self):
        self._click(self.comfort_button)

    def is_comfort_selected(self):
        element = self._find(self.comfort_button)
        return "active" in element.get_attribute("class")

        # ============================================================
        # MÉTODOS — COMFORT
        # ============================================================

    def is_comfort_open(self):
        return "Sorvete" in self.driver.page_source

        # ============================
        # MÉTODOS - TELEFONE
        # ============================

    def open_phone_modal(self):
        self._click(self.phone_button)

    def fill_phone_number(self, phone):
        self._type(self.phone_input, phone)

    def click_next_phone(self):
        self._click(self.next_phone_button)

    def wait_phone_modal_close(self):
        self.wait.until(EC.invisibility_of_element_located(self.phone_modal))

        # ============================
        # MÉTODOS - CARTÃO
        # ============================
    def click_close_card_modal_button(self):
        self._click(self.close_card_modal_button)

    def add_card(self, number, cvv):

        # Abrir modal de pagamento
        self._click(self.payment_button)
        time.sleep(1)

        # Abrir modal de adicionar cartão
        self._click(self.add_card_button)
        time.sleep(1)

        # Preencher número do cartão
        number_field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        number_field.clear()
        number_field.send_keys(number)
        time.sleep(0.5)

        # Preencher CVV
        cvv_field = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        cvv_field.clear()
        cvv_field.send_keys(cvv)
        time.sleep(0.5)

        # Perder o foco do CVV
        cvv_field.send_keys(Keys.TAB)
        time.sleep(1)

        # Clicar no botão Adicionar
        btn = self.wait.until(EC.element_to_be_clickable(self.card_add_confirm))
        btn.click()

        # Esperar o modal fechar
        self.click_close_card_modal_button()

    def select_saved_card(self):
            card = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'pp-card')]"))
            )
            card.click()

        # ============================
        # Comentario
        # ============================
    def wait_main_screen(self):
        pedir_button = (By.XPATH, "//button[contains(text(),'Pedir')]")
        self.wait.until(EC.visibility_of_element_located(pedir_button))

    def wait_comment_field(self):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='comment']"))
        )


    # ============================
    # MÉTODOS - SMS
    # ============================

    def fill_sms_code(self, code):
        field = self.wait.until(EC.visibility_of_element_located(self.sms_input))
        field.clear()
        field.send_keys(code)

    def confirm_sms(self):
        self._click(self.sms_confirm_button)

    def wait_phone_modal_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.phone_modal))
        except:
            pass

    def wait_for_sms_input(self):
        self.wait.until(EC.visibility_of_element_located(self.sms_input))

    # ============================
    # MÉTODOS - EXTRAS
    # ============================
    def set_message_for_driver(self, message):
            # Preenche a mensagem personalizada que será enviada ao motorista
            self._type(self.MESSAGE_FOR_DRIVER_FIELD, message)

    def get_message_for_driver(self):
            # Retorna a mensagem que está preenchida no campo
            return self._get_value(self.MESSAGE_FOR_DRIVER_FIELD)

    #def get_message_for_drive(self, text):
        #comment_input = self.wait.until(EC.visibility_of_element_located(self.comment_field))
        #comment_input.clear()
        #comment_input.send_keys(text)
        #return self._get_value(self.MESSAGE_FOR_DRIVER_FIELD)

    def open_extras(self):
        self._click(self.extras_button)

    def click_blanket_and_handkerchiefs_option(self):
        # Marca a opção de cobertor e lençóis
        self._click(self.BLANKET_AND_HANDKERCHIEFS_OPTION_DIV)

    def is_blanket_and_handkerchiefs_option_checked(self):
        # Verifica se a opção está marcada
        return self._find(self.BLANKET_AND_HANDKERCHIEFS_OPTION_INPUT).is_selected()

    # ============================================================
    # MÉTODOS — SORVETE E SABORES
    # ============================================================

    def flavor_plus(self, flavor):
        return (
            By.XPATH,
            f"//div[@class='r-counter-label' and text()='{flavor}']"
            f"/following::div[@class='counter-plus'][1]"
        )

    def flavor_value(self, flavor):
        return (
            By.XPATH,
            f"//div[@class='r-counter-label' and text()='{flavor}']"
            f"/following::div[@class='counter-value'][1]"
        )

    def wait_for_flavor(self, flavor):
        self.wait.until(
            EC.presence_of_element_located(self.flavor_value(flavor))
        )

    def get_flavor_count(self, flavor):
        locator = self.flavor_value(flavor)
        return int(self._find(locator).text)

    def add_flavor_quantity(self, flavor, target_quantity):
        current = self.get_flavor_count(flavor)

        if current >= target_quantity:
            return

        clicks_needed = target_quantity - current

        for _ in range(clicks_needed):
            plus_button = self._find(self.flavor_plus(flavor))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", plus_button
            )
            self.wait.until(EC.element_to_be_clickable(self.flavor_plus(flavor)))
            plus_button.click()
            time.sleep(0.3)

    # ============================================================
    # PEDIR TÁXI (ETAPA 8)
    # ============================================================

    def order_taxi(self):
        self._click(self.order_button)
        return self._find(self.modal_search)