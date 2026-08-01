package com.parabank.api.tests;

import com.parabank.api.base.BaseApiTest;
import com.parabank.api.specs.ApiSpecs;
import utils.ConfigReader;

import io.restassured.response.Response;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

public class LoginApiTest extends BaseApiTest {

    @Test
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