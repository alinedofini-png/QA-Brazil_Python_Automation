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
        time.sleep(2)

        page.select_comfort()
        time.sleep(2)

        page.open_phone_modal()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_next_phone()

        sms_code = retrieve_phone_code(page.driver)
        page.fill_sms_code(sms_code)
        page.confirm_sms()
        page.wait_phone_modal_disappear()
        time.sleep(1)

        page.add_card(data.CARD_NUMBER, data.CARD_CODE)

        # ✅ Assert: método de pagamento visível na tela
        assert page.driver.find_element(*page.payment_button).is_displayed()

    # ============================================================
    # 5️⃣ Comentário
    # ============================================================
    def test_write_message_for_driver(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        page.click_taxi()
        time.sleep(1)

        page.select_comfort()
        time.sleep(1)

        # ✅ Método correto
        page.set_message_for_driver(self.MESSAGE_FOR_DRIVER)
        time.sleep(1)

        # ✅ Assert via getter, não page_source
        assert page.get_message_for_driver() == data.MESSAGE_FOR_DRIVER

    # ============================================================
    # 6️⃣ Cobertor e lençóis
    # ============================================================
    def test_tissues_in_comfort(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        page.click_taxi()
        time.sleep(1)

        page.select_comfort()
        time.sleep(1)

        page.click_blanket_and_handkerchiefs_option()

        assert page.is_blanket_and_handkerchiefs_option_checked() is True

    # ============================================================
    # 7️⃣ Sorvete
    # ============================================================
    def test_add_ice_cream(self):
        page = self.open_page()

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(1)

        page.click_taxi()
        time.sleep(1)

        page.select_comfort()
        time.sleep(1)

        page.wait_for_flavor("Sorvete")
        page.add_flavor_quantity("Sorvete", 2)

        assert page.get_flavor_count("Sorvete") == 2

    # ============================================================
    # 8️⃣ Fluxo completo
    # ============================================================
    def test_order_taxi(self):
        page = self.open_page()

        # 1. Rota
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(1)

        # 2. Abrir painel
        page.click_taxi()
        time.sleep(1)

        # 3. Comfort
        page.select_comfort()
        time.sleep(1)

        # 4. Telefone + SMS
        page.open_phone_modal()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_next_phone()

        page.wait_for_sms_input()
        sms_code = retrieve_phone_code(page.driver)
        page.fill_sms_code(sms_code)
        page.confirm_sms()
        page.wait_phone_modal_close()

        # 5. Cartão
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)

        # 6. Esperar tela principal + campo de comentário
        page.wait_main_screen()
        page.wait_comment_field()


        # 7. Cobertor e lenços
        page.open_extras()
        page.wait_overlay_disappear()
        page.click_blanket_and_handkerchiefs_option()

        assert page.is_blanket_and_handkerchiefs_option_checked()

        # 8. Sorvete (2 unidades)
        page.wait_for_flavor("Sorvete")
        page.add_flavor_quantity("Sorvete", 2)

        # 9. Pedir táxi
        modal = page.order_taxi()

        # 10. Verificações finais
        assert modal.is_displayed(), "A modal de busca não apareceu"
        assert data.MESSAGE_FOR_DRIVER in page.driver.page_source, \
            "A mensagem para o motorista não foi incluída"