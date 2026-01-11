"""
Web Steps

Steps file for web interactions with Selenium
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Check that text is not on the page"""
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set an input field to a specific value"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select an option from a dropdown"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Check that a dropdown has a specific value selected"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Check that an input field is empty"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == ''


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy the value of an input field to the clipboard"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste the value from the clipboard into an input field"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clear button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button by its name"""
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{name}" in the "{element_name}" field')
def step_impl(context, name, element_name):
    """Check that an input field contains a specific value"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            name
        )
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change the value of an input field"""
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by 'product_' so the Name field has an id='product_name'
# We can then lowercase the name and prefix with product_ to get the id
##################################################################


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check for a message in the flash message area"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Check if a name appears in the search results"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Check that a name does not appear in the search results"""
    element = context.driver.find_element(By.ID, 'search_results')
    assert name not in element.text