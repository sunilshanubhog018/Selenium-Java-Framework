package com.parabank.api.tests;

import com.parabank.api.base.BaseApiTest;
import com.parabank.api.specs.ApiSpecs;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import utils.ConfigReader;

import io.restassured.response.Response;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

@Epic("Banking Application")
@Feature("API - Authentication")
public class LoginApiTest extends BaseApiTest {

    @Test(groups = {"smoke", "api"})
    @Story("Valid login returns customer")
    public void loginWithValidCredentials_returnsCustomer() {
        String username = ConfigReader.get("api.username");
        String password = ConfigReader.get("api.password");

        Response response =
            given()
                .spec(ApiSpecs.requestSpec())
            .when()
                .get("/login/" + username + "/" + password)
            .then()
                .spec(ApiSpecs.responseSpec200())
                .body("id", notNullValue())
                .body("firstName", equalTo("John"))
                .body("lastName", equalTo("Smith"))
                .extract().response();

        System.out.println("Logged in customer id: " + response.jsonPath().getString("id"));
        System.out.println("First name: " + response.jsonPath().getString("firstName"));
    }
}