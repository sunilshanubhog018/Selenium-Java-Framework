package com.parabank.api.tests;

import com.parabank.api.base.BaseApiTest;
import com.parabank.api.specs.ApiSpecs;

import io.restassured.response.Response;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

public class LoginApiTest extends BaseApiTest {

    @Test
    public void loginWithValidCredentials_returnsCustomer() {

        Response response =
            given()
                .spec(ApiSpecs.requestSpec())
            .when()
                .get("/login/john/demo")
            .then()
                .spec(ApiSpecs.responseSpec200())          // expects 200 + logs response
                .body("id", notNullValue())                // customer id came back
                .body("firstName", equalTo("John"))
                .body("lastName", equalTo("Smith"))
                .extract().response();

        // Assertion lives in the test - same discipline as your UI tests
        System.out.println("Logged in customer id: " + response.jsonPath().getString("id"));
        System.out.println("First name: " + response.jsonPath().getString("firstName"));
    }
}