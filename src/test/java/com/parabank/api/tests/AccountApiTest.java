package com.parabank.api.tests;

import com.parabank.api.base.BaseApiTest;
import com.parabank.api.specs.ApiSpecs;

import io.restassured.response.Response;
import io.restassured.path.json.JsonPath;
import org.testng.annotations.Test;

import java.util.List;

import static io.restassured.RestAssured.given;




public class AccountApiTest extends BaseApiTest {

    @Test
    public void getCustomerAccounts_returnsAccountList() {

        Response response =
            given()
                .spec(ApiSpecs.requestSpec())
            .when()
                .get("/customers/12212/accounts")
            .then()
                .spec(ApiSpecs.responseSpec200())
                .extract().response();

        // Print the whole response so we can SEE the account array structure
        System.out.println("Accounts response: " + response.asString());
        
     // ===== new lines below =====
        JsonPath js = response.jsonPath();

        int accountCount = js.getList("$").size();
        System.out.println("Total accounts: " + accountCount);

        int firstAccountId = js.getInt("[0].id");
        System.out.println("First account id: " + firstAccountId);

        List<Integer> allIds = js.getList("id");
        System.out.println("All account ids: " + allIds);
    }
}