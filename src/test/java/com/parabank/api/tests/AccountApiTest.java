package com.parabank.api.tests;

import com.parabank.api.base.BaseApiTest;
import com.parabank.api.specs.ApiSpecs;
import utils.ConfigReader;

import io.restassured.response.Response;
import io.restassured.path.json.JsonPath;
import org.testng.annotations.Test;

import java.util.List;

import static io.restassured.RestAssured.given;

public class AccountApiTest extends BaseApiTest {

    @Test
    public void getCustomerAccounts_returnsAccountList() {
        String customerId = ConfigReader.get("api.customer.id");

        Response response =
            given()
                .spec(ApiSpecs.requestSpec())
            .when()
                .get("/customers/" + customerId + "/accounts")
            .then()
                .spec(ApiSpecs.responseSpec200())
                .extract().response();

        System.out.println("Accounts response: " + response.asString());

        JsonPath js = response.jsonPath();
        int accountCount = js.getList("$").size();
        System.out.println("Total accounts: " + accountCount);

        int firstAccountId = js.getInt("[0].id");
        System.out.println("First account id: " + firstAccountId);

        List<Integer> allIds = js.getList("id");
        System.out.println("All account ids: " + allIds);
    }
}