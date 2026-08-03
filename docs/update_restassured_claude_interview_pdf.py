"""Rebuild RestAssured_API_Interview_QA_claude.pdf with light accuracy polish.

Original Claude guide was already excellent (fundamentals + senior banking + MCQs).
Polish focus: specs vs static baseURI, schema dependency, token manager, BigDecimal money,
idempotency keys, PII log redaction, parallel data isolation, clean answer key layout.
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted, ListFlowable, ListItem
)

OUT = Path(
    r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material"
    r"\CLAUDE AI NOTES\REST ASSURED API AUTOAMTION NOTES"
    r"\RestAssured_API_Interview_QA_claude.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
GREEN = HexColor("#166534")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")
RED = HexColor("#9f1239")
BLUE = HexColor("#1d4ed8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14.5,
                          leading=18, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=8.6,
                          leading=11.2, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=10.5,
                          leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9,
                          leading=11, textColor=TEAL, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.1,
                          leading=10.3, textColor=NAVY, spaceBefore=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=7.7,
                          leading=9.8, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.0,
                          leading=8.9, textColor=GOLD, leftIndent=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=6.9,
                          leading=8.8, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=7.8,
                          leading=9.9, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.0,
                          leading=7.6, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=6.6,
                          leading=8.3, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=6.6,
                          leading=8.3, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=BLUE, spaceAfter=1))
styles.add(ParagraphStyle(name="LvlM", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=TEAL, spaceAfter=1))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=RED, spaceAfter=1))
styles.add(ParagraphStyle(name="MCQ", fontName="Helvetica", fontSize=7.4,
                          leading=9.4, textColor=DARK, spaceAfter=0.5))
styles.add(ParagraphStyle(name="MCQO", fontName="Helvetica", fontSize=7.1,
                          leading=9.0, textColor=MUTED, leftIndent=10, spaceAfter=0.3))
styles.add(ParagraphStyle(name="RFQ", fontName="Helvetica-Bold", fontSize=7.2,
                          leading=9.2, textColor=NAVY, spaceAfter=0.5))
styles.add(ParagraphStyle(name="RFA", fontName="Helvetica", fontSize=7.1,
                          leading=9.0, textColor=DARK, leftIndent=6, spaceAfter=2))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Tip:</b> {t}", "DTip")


def polish(t):
    return P(f"<b>Polish:</b> {t}", "DFix")


def hline():
    return HRFlowable(width="100%", thickness=0.35, color=SOFT, spaceBefore=1, spaceAfter=2)


def qa(n, q, parts):
    items = [P(f"Q{n}. {q}", "DQ")]
    for p in parts:
        items.append(P(p, "DA") if isinstance(p, str) else p)
    return KeepTogether(items)


def mcq(n, q, opts):
    items = [P(f"<b>Q{n}.</b> {q}", "MCQ")]
    for o in opts:
        items.append(P(o, "MCQO"))
    return KeepTogether(items)


def rf(n, q, a):
    return KeepTogether([P(f"{n}. {q}", "RFQ"), P(a, "RFA")])


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12, A4[0], 12, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 6.3)
        canvas.drawString(26, A4[1] - 8, "REST Assured API Automation | SDET Interview Q&A")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "Fundamentals · Senior · Practice")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.3)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def mini_table(headers, rows, widths):
    data = [[P(h, "DHead") for h in headers]]
    for r in rows:
        data.append([P(c, "DCell") for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
    ]))
    return t


def build():
    story = []

    # ── COVER ──────────────────────────────────────────────
    cover = Table([
        [P("REST Assured API Automation", "TMain")],
        [P("SDET Interview Question Bank<br/>"
           "Banking / fintech domain focus · ParaBank examples throughout<br/><br/>"
           "PART 1 Fundamentals (28) &nbsp;·&nbsp; PART 2 Senior / Framework (29 + rapid fire)<br/>"
           "PART 3 Practice Tests (5 × 10 MCQs = 50) + Answer Key",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 28))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Original Claude guide was already excellent. Verified and lightly polished for interview accuracy "
        "and banking real-world depth.",
        "DBody"
    ))
    story.append(polish(
        "RequestSpec over static baseURI (parallel-safe); json-schema-validator dependency; TokenManager + "
        "sync refresh; HTTP 200 vs business status; BigDecimal money (not double); idempotency keys; "
        "PII masking filters; clean MCQ answer key."
    ))
    story.append(P(
        "How to use: answer first, then read. Practice every coding snippet in IDE. For senior rounds, "
        "lead with architecture and banking risk (money movement, authZ, compliance), not only syntax.",
        "DBody"
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PART 1 — FUNDAMENTALS
    # ═══════════════════════════════════════════════════════
    story.append(P("PART 1 — Fundamentals", "DH1"))
    story.append(P("Core concepts every API tester must know cold", "LvlB"))
    story.append(hline())

    story.append(qa(1, "What is an API, and how is API testing different from UI testing?", [
        "An API (Application Programming Interface) is the contract that lets two software systems talk to each "
        "other. In a banking app, the UI is the web page a customer sees; the API is the service layer underneath "
        "that actually moves money, fetches balances, and creates accounts.",
        "API testing hits that service layer directly over HTTP, without a browser. It is faster (no page loads, no "
        "rendering), more stable (no locators to break when the UI changes), and can test logic the UI never "
        "exposes. UI testing validates what the user sees; API testing validates business logic and data contracts.",
    ]))

    story.append(qa(2, "What is REST, and how does it differ from SOAP?", [
        "REST (Representational State Transfer) is an architectural style: resource-based, standard HTTP methods, "
        "stateless, typically JSON. SOAP is a stricter protocol: XML-only, WSDL contract, built-in security/transaction "
        "standards, heavier. Banks still run SOAP for legacy core systems; newer services are almost always REST.",
        "Key differences: REST is lightweight and flexible; SOAP is rigid but has formal contracts and SOAP faults.",
    ]))

    story.append(qa(3, "Explain the main HTTP methods and when each is used.", [
        "<b>GET</b> — retrieve data; must not change server state (safe and idempotent). E.g. fetch account balance.",
        "<b>POST</b> — create a resource or trigger an action. Not idempotent — calling twice creates two things. "
        "E.g. transfer funds, open an account.",
        "<b>PUT</b> — replace a resource entirely. Idempotent. E.g. update full customer profile.",
        "<b>PATCH</b> — partially update a resource. E.g. change only the phone number.",
        "<b>DELETE</b> — remove a resource. Idempotent by design (repeat delete → same end state).",
        tip("Idempotency matters enormously in banking: a retried POST /transfer could move money twice — real "
            "payment APIs use Idempotency-Key headers."),
    ]))

    story.append(qa(4, "What are the important HTTP status codes an API tester must know?", [
        "<b>2xx Success:</b> 200 OK, 201 Created, 202 Accepted (queued, not finished), 204 No Content.",
        "<b>3xx:</b> 301 Moved Permanently, 304 Not Modified.",
        "<b>4xx Client:</b> 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, "
        "422 Unprocessable Entity, 429 Too Many Requests.",
        "<b>5xx Server:</b> 500, 502, 503, 504 Gateway Timeout.",
        tip("Interview trap: 401 = 'I do not know who you are'; 403 = 'I know who you are, and you are not allowed'."),
    ]))

    story.append(qa(5, "Explain the given / when / then syntax in REST Assured.", [
        "REST Assured uses a BDD-style fluent chain:",
        "<b>given()</b> — setup: headers, query/path params, body, authentication.",
        "<b>when()</b> — action: HTTP method and endpoint, e.g. .post(\"/transfer\").",
        "<b>then()</b> — validation: status code, body assertions, response time, extraction.",
        code('RestAssured.baseURI = "https://parabank.parasoft.com";\n'
             'given()\n'
             '    .queryParam("accountId", 13344)\n'
             '    .header("Content-Type", "application/json")\n'
             '.when()\n'
             '    .get("/parabank/services/bank/accounts/13344")\n'
             '.then()\n'
             '    .statusCode(200)\n'
             '    .body("type", equalTo("SAVINGS"));'),
        polish("Prefer RequestSpecification over mutating RestAssured.baseURI in frameworks / parallel runs."),
    ]))

    story.append(qa(6, "Where exactly is the HTTP method specified in a REST Assured chain?", [
        "In the method call right after .when(). The method name IS the HTTP verb — .get(), .post(), .put(), "
        ".delete(). The string passed is only the endpoint path, never the verb.",
        "Common beginner mistake: .get(\"GET /accounts/123\") — puts the literal word GET into the URL. "
        "Correct: .get(\"/accounts/123\").",
    ]))

    story.append(qa(7, "What is JsonPath and why can you not just use String methods to read a response?", [
        "A response arrives as plain text. To Java it is just a String — it has no idea that place_id is a field. "
        "Parsing converts that flat text into a navigable structure you can query by key.",
        "String searching fails because spacing varies, keys may nest, and values contain commas/quotes/braces. "
        "JsonPath lets you address values by path.",
        code('JsonPath js = response.jsonPath();\n'
             'String type    = js.getString("type");\n'
             'float  balance = js.getFloat("balance");\n'
             'int    firstId = js.getInt("[0].id");\n'
             'List<Integer> ids = js.getList("id");\n'
             'int count = js.getList("$").size();'),
    ]))

    story.append(qa(8, "How do you extract a value from a response and use it in the next request?", [
        "Use .extract() to bridge from validation to usage. Critically, assign the extracted value to a variable — "
        "calling .extract() without assignment silently discards the result.",
        "This chaining is the backbone of API test flows: create → capture ID → GET / PUT / DELETE.",
        code('Response response =\n'
             '    given().spec(requestSpec())\n'
             '    .when().get("/customers/12212/accounts")\n'
             '    .then().statusCode(200)\n'
             '    .extract().response();\n'
             'int accountId = response.jsonPath().getInt("[0].id");\n'
             '// accountId feeds next request — never hardcode'),
    ]))

    story.append(qa(9, "What is the difference between a path parameter and a query parameter?", [
        "A <b>path parameter</b> is part of the URL structure and identifies a specific resource: "
        "/accounts/13344 — here 13344 is a path param.",
        "A <b>query parameter</b> comes after ? and filters or supplies extra data: "
        "/transfer?fromAccountId=13344&amp;toAccountId=54321&amp;amount=100",
        "Rule of thumb: path params identify <i>which</i> resource; query params modify <i>how</i> or supply action inputs.",
        code('given()\n'
             '    .pathParam("accountId", 13344)\n'
             '    .queryParam("amount", 100)\n'
             '.when()\n'
             '    .get("/accounts/{accountId}");'),
    ]))

    story.append(qa(10, "How do you validate a JSON response body in REST Assured?", [
        "Use .body() with Hamcrest matchers. Assert on simple fields, nested fields with dot notation, and "
        "array elements by index or collection matchers. Always read the actual response before writing assertions.",
        code('.then()\n'
             '    .statusCode(200)\n'
             '    .body("firstName", equalTo("John"))\n'
             '    .body("address.city", equalTo("Beverly Hills"))\n'
             '    .body("id", notNullValue())\n'
             '    .body("accounts.size()", greaterThan(0))\n'
             '    .body("type", hasItems("CHECKING", "SAVINGS"));'),
    ]))

    story.append(qa(11, "What is serialization and deserialization in API testing?", [
        "<b>Serialization</b> — Java object → JSON request body (POJO → Jackson → JSON).",
        "<b>Deserialization</b> — JSON response → Java object so you call getters instead of scraping strings.",
        code('// Serialization\n'
             'Payee payee = new Payee("Electric Co", address, "555-1234", "98765");\n'
             'given().body(payee).when().post("/billpay");\n'
             '// Deserialization\n'
             'Account account = response.as(Account.class);\n'
             'System.out.println(account.getBalance());'),
    ]))

    story.append(qa(12, "What is a POJO and why use it instead of JsonPath?", [
        "A POJO (Plain Old Java Object) is a simple class whose fields mirror the JSON structure, with getters/setters.",
        "Advantages: compile-time safety (typo in getBalance() fails to compile vs runtime JsonPath typo); "
        "refactorable; readable; reusable for request and response.",
        code('public class Account {\n'
             '    private int id;\n'
             '    private int customerId;\n'
             '    private String type;\n'
             '    private BigDecimal balance;  // prefer BigDecimal for money\n'
             '    // getters and setters\n'
             '}'),
    ]))

    story.append(qa(13, "How do you handle authentication in REST Assured?", [
        "Basic: .auth().basic(\"user\", \"pass\")",
        "Preemptive Basic: .auth().preemptive().basic(\"user\", \"pass\") — sends credentials without waiting for 401.",
        "Bearer: .header(\"Authorization\", \"Bearer \" + token)",
        "OAuth 2.0: .auth().oauth2(accessToken)",
        "API Key: usually a header or query param.",
        polish("Fetch token via TokenManager (cache + expiry + synchronized refresh). Inject into RequestSpec. "
               "Never hardcode tokens — env vars / CI secrets / vault."),
    ]))

    story.append(qa(14, "What is a RequestSpecification and why use spec builders?", [
        "A RequestSpecification bundles common request setup — base URI, base path, headers, content type, "
        "logging, auth — into one reusable object. A ResponseSpecification does the same for common expectations.",
        "API equivalent of a BasePage: define once, reuse everywhere; when base URI changes you edit one place.",
        code('public static RequestSpecification requestSpec() {\n'
             '    return new RequestSpecBuilder()\n'
             '        .setBaseUri(ConfigReader.get("api.base.uri"))\n'
             '        .setBasePath(ConfigReader.get("api.base.path"))\n'
             '        .setContentType(ContentType.JSON)\n'
             '        .addFilter(new MaskingFilter())\n'
             '        .log(LogDetail.ALL)\n'
             '        .build();\n'
             '}\n'
             'given().spec(ApiSpecs.requestSpec()).when().get("/accounts/13344");'),
        tip("Prefer specs over RestAssured.baseURI statics for parallel safety."),
    ]))

    story.append(qa(15, "How do you log requests and responses in REST Assured?", [
        "Logging is essential for debugging — when a call returns 400, you need to see exactly what was sent.",
        "• .log().all() after given() logs the full request",
        "• .log().all() after then() logs the full response",
        "• .log().ifValidationFails() logs only on failure — best for CI, keeps logs clean",
        "• RestAssured.filters(new RequestLoggingFilter(), new ResponseLoggingFilter()) applies globally",
        code('given().log().all()\n'
             '.when().get("/accounts/13344")\n'
             '.then().log().ifValidationFails()\n'
             '       .statusCode(200);'),
        tip("In banking, never log Authorization or PII raw — use a MaskingFilter (see senior section)."),
    ]))

    story.append(qa(16, "What is JSON Schema validation and why does it matter?", [
        "Schema validation checks structure — field names, data types, required fields, nesting — rather than "
        "specific values. Catches contract breaks value assertions miss (balance becomes a string; field dropped).",
        polish("Dependency required: io.rest-assured:json-schema-validator (not on default rest-assured alone)."),
        code('.then()\n'
             '  .assertThat()\n'
             '  .body(matchesJsonSchemaInClasspath("schemas/account-schema.json"));'),
    ]))

    story.append(qa(17, "How do you assert on response time?", [
        "Useful as a lightweight guard against regressions — not a substitute for load testing (JMeter/Gatling).",
        code('.then()\n'
             '    .time(lessThan(2000L));  // under 2 seconds\n'
             'long ms = response.getTime();\n'
             'long sec = response.getTimeIn(TimeUnit.SECONDS);'),
        tip("Use env-specific thresholds; UAT slowness is often capacity, not a product bug."),
    ]))

    story.append(qa(18, "What is the difference between @BeforeClass, @BeforeMethod and @BeforeSuite?", [
        "<b>@BeforeSuite</b> — once for entire suite. Token bootstrap, shared expensive setup.",
        "<b>@BeforeClass</b> — once per test class. Class-scoped Rest Assured config.",
        "<b>@BeforeMethod</b> — before every test. Per-test data isolation.",
        "API frameworks usually need less per-method setup than UI (no browser to reset) — one reason suites are fast.",
    ]))

    story.append(qa(19, "What is a request payload, and which HTTP methods carry one?", [
        "The payload (body) is the data sent with a request — usually JSON in modern REST APIs.",
        "POST, PUT and PATCH carry payloads. GET and DELETE normally do not. A GET body is technically allowed "
        "by the HTTP spec but widely ignored by servers and proxies — put identifying data in path/query params.",
        tip("If asked to write a GET with a body, point out identifying data belongs in the URL."),
    ]))

    story.append(qa(20, "What is the difference between Content-Type and Accept headers?", [
        "<b>Content-Type</b> describes the format of data you are sending. "
        "<b>Accept</b> tells the server the format you want back. They are independent.",
        "ParaBank, for instance, can return XML or JSON depending on the Accept header.",
        code('given()\n'
             '    .contentType(ContentType.JSON)   // I am sending JSON\n'
             '    .accept(ContentType.JSON)        // send me JSON back\n'
             '    .body(transferRequest)\n'
             '.when()\n'
             '    .post("/transfer");'),
    ]))

    story.append(qa(21, "What are the different parameter types in REST Assured?", [
        "• <b>queryParam</b> — after ?; filters or action inputs",
        "• <b>pathParam</b> — substituted into URL template; identifies resource",
        "• <b>formParam</b> — form-encoded body (login forms)",
        "• <b>header</b> — Authorization and other headers",
        "• <b>multiPart</b> — file uploads (multipart/form-data)",
        "Using the wrong type is a common cause of a puzzling 400 (e.g. form params to a JSON endpoint).",
        code('given()\n'
             '    .pathParam("accountId", 13344)\n'
             '    .queryParam("startDate", "2026-01-01")\n'
             '    .header("Authorization", "Bearer " + token)\n'
             '.when()\n'
             '    .get("/accounts/{accountId}/transactions");'),
    ]))

    story.append(qa(22, "What is GPath and how does it differ from JsonPath syntax from other tools?", [
        "REST Assured uses Groovy GPath for body() assertions and JsonPath extraction — not the Jayway/Postman "
        "JsonPath syntax (which starts with $. and uses bracket filters).",
        "GPath uses plain dot notation and Groovy collection methods. Copying a Postman expression straight into "
        "REST Assured often fails. GPath supports filtering, aggregation and projection (senior section).",
        code('// GPath (REST Assured)\n'
             'js.getString("address.city");\n'
             'js.getInt("[0].id");\n'
             '// NOT Jayway: $.address.city   $[0].id'),
    ]))

    story.append(qa(23, "How do you extract headers, cookies and the status line from a response?", [
        "Beyond the body, response metadata is often worth asserting — especially security headers and session "
        "cookies in banking applications.",
        code('Response r = given().when().get("/accounts/13344");\n'
             'String contentType = r.getHeader("Content-Type");\n'
             'String sessionId   = r.getCookie("JSESSIONID");\n'
             'int    status      = r.getStatusCode();\n'
             'String statusLine  = r.getStatusLine();\n'
             'long   timeTaken   = r.getTime();\n'
             'r.then().header("X-Content-Type-Options", equalTo("nosniff"));'),
    ]))

    story.append(qa(24, "How do you handle XML responses in REST Assured?", [
        "Use XmlPath instead of JsonPath. Many banking core systems still expose SOAP or XML REST services.",
        code('XmlPath xml = new XmlPath(response.asString());\n'
             'String accountType = xml.getString("account.type");\n'
             '.then().body("account.balance", equalTo("1231.10"));'),
    ]))

    story.append(qa(25, "What is Hamcrest and why does REST Assured use it?", [
        "Hamcrest is a matcher library that makes assertions read like English and produce clear failure messages. "
        "REST Assured's body() method takes Hamcrest matchers.",
        "Common: equalTo, not, notNullValue, hasItem, hasItems, hasSize, greaterThan, lessThan, "
        "containsString, everyItem.",
        tip("TestNG may ship its own Hamcrest; version clash can cause NoSuchMethodError — pin one explicit Hamcrest."),
        code('.body("balance", greaterThan(0f))\n'
             '.body("type", not(equalTo("CLOSED")))\n'
             '.body("accounts", hasSize(11))\n'
             '.body("transactions.amount", everyItem(greaterThan(0f)))'),
    ]))

    story.append(qa(26, "What are the main types of API testing?", [
        "• <b>Functional</b> — does the endpoint do what the specification says",
        "• <b>Contract / schema</b> — structure, field names, data types",
        "• <b>Integration</b> — chained services end to end",
        "• <b>Security</b> — authN, authZ, injection, data exposure",
        "• <b>Performance / load</b> — response time under concurrency (usually JMeter/Gatling)",
        "• <b>Negative / error handling</b> — invalid input, boundaries, failure modes",
        "In automation you primarily build functional, contract and negative coverage.",
    ]))

    story.append(qa(27, "Why is relaxed HTTPS validation sometimes needed, and what is the risk?", [
        "Test environments often use self-signed or expired certificates → SSL handshake exception. "
        "RestAssured.useRelaxedHTTPSValidation() bypasses certificate verification.",
        "Risk: disables a genuine security check. Acceptable in controlled test envs; never for production-facing "
        "tests; make it config-driven so it can be switched off per environment.",
        code('if (Boolean.parseBoolean(ConfigReader.get("api.relaxed.ssl"))) {\n'
             '    RestAssured.useRelaxedHTTPSValidation();\n'
             '}'),
    ]))

    story.append(qa(28, "What is the difference between asserting inside then() and using TestNG Assert?", [
        "then() assertions are fluent, fail fast, and produce REST Assured's detailed expected vs actual output. "
        "Best for validating the response itself.",
        "TestNG Assert is used after extraction when you need values computed in the test — balance delta, "
        "API vs DB comparison. SoftAssert collects several failures in one run.",
        "A mature test uses both: then() for response contract, TestNG Assert for business logic verification.",
    ]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PART 2 — SENIOR / FRAMEWORK
    # ═══════════════════════════════════════════════════════
    story.append(P("PART 2 — Senior / Framework Level", "DH1"))
    story.append(P("Architecture, banking scenarios, edge cases and behavioural questions", "LvlR"))
    story.append(hline())

    story.append(qa(1, "Walk me through the architecture of the API automation framework you built.", [
        "Layered structure inside a single Maven project, sharing infrastructure with the UI framework:",
        "• <b>config</b> — properties + ConfigReader; URIs/credentials never hardcoded",
        "• <b>specs</b> — RequestSpecification / ResponseSpecification builders",
        "• <b>base</b> — BaseApiTest: global filters, optional SSL config",
        "• <b>payloads</b> — request/response POJOs (BigDecimal for money fields)",
        "• <b>endpoints / services</b> — AccountService, TransactionService, BillPayService; every URL lives here",
        "• <b>tests</b> — smoke + regression; orchestration and assertions only",
        "• <b>utils</b> — data providers, TokenManager, schema validators, Awaitility helpers",
        "Governing rule: no test class contains a raw endpoint URL, exactly as no UI test contains a locator.",
    ]))

    story.append(qa(2, "Why keep the API layer in the same project as the UI framework?", [
        "1. Shared infrastructure — one ConfigReader, one reporting setup, one CI pipeline.",
        "2. Consistent conventions — one build, one dependency set.",
        "3. <b>API can serve UI setup</b> — instead of registering a user through six UI screens, create via API, "
        "then drive only the behaviour under test through the browser. Cuts UI suite runtime and flakiness.",
    ]))

    story.append(qa(3, "BANKING: How would you test a fund transfer API properly?", [
        "A 200 proves nothing about whether money moved. Pattern: read, act, re-read, assert deltas:",
        "1. GET source balance before  2. GET destination before  3. POST transfer  "
        "4. GET both again  5. Assert source −amount, destination +amount",
        "Then ledger: debit on source, credit on destination, matching amounts/timestamps.",
        "Also cover: insufficient funds, closed/frozen accounts, negative/zero amounts, &gt;2 decimal places, "
        "same-account transfer, daily limit boundary, <b>duplicate submission / idempotency</b>.",
        code('BigDecimal fromBefore = accountService.getBalance(fromId);\n'
             'BigDecimal toBefore   = accountService.getBalance(toId);\n'
             'transactionService.transfer(fromId, toId, new BigDecimal("100.00"))\n'
             '    .then().statusCode(200).body("status", equalTo("SUCCESS"));\n'
             'BigDecimal fromAfter = accountService.getBalance(fromId);\n'
             'BigDecimal toAfter   = accountService.getBalance(toId);\n'
             'Assert.assertEquals(0, fromAfter.compareTo(fromBefore.subtract(new BigDecimal("100.00"))));\n'
             'Assert.assertEquals(0, toAfter.compareTo(toBefore.add(new BigDecimal("100.00"))));'),
        polish("Original sample used double; money assertions should use BigDecimal + compareTo."),
    ]))

    story.append(qa(4, "BANKING: API returns 200 OK but body says status FAILED. How do you handle this?", [
        "HTTP status describes transport; response body describes business outcome. A payment gateway can accept "
        "your request (200) while the payment itself was declined.",
        "A test that only asserts status code would pass on a failed transaction — false negative.",
        "Assert both layers: transport status AND business status, plus actual state change.",
        code('.then()\n'
             '    .statusCode(200)\n'
             '    .body("status", equalTo("SUCCESS"))\n'
             '    .body("transactionId", notNullValue());\n'
             '// then re-read balance to confirm state actually changed'),
    ]))

    story.append(qa(5, "How do you handle test data in an API framework (especially banking)?", [
        "Maturity ladder: hardcoded (avoid) → externalised Excel/JSON/CSV DataProvider → "
        "dynamically created via API in setup + cleanup → database seeded known state.",
        "Banking makes this acute: balances are mutable and shared. If a test asserts balance 1000 while another "
        "transferred out, you get intermittent failures that are not product defects.",
        tip("Rule: a test should create and own the data it asserts on; never depend on data another test can mutate."),
    ]))

    story.append(qa(6, "How would you design tests to run in parallel safely?", [
        "• Independent data per thread — each test creates its own account (biggest factor)",
        "• No shared mutable statics — auth token via ThreadLocal or TokenManager with synchronized refresh",
        "• Prefer RequestSpecification over RestAssured.baseURI global mutable state",
        "• testng.xml: parallel=\"methods\" or \"classes\" with sensible thread-count",
        "• Watch the server — 20 threads can rate-limit or overwhelm a test environment",
        code('<suite name="API Regression" parallel="methods" thread-count="5">\n'
             '  <test name="Banking API Tests">\n'
             '    <classes>\n'
             '      <class name="com.parabank.api.tests.TransferApiTest"/>\n'
             '    </classes>\n'
             '  </test>\n'
             '</suite>'),
    ]))

    story.append(qa(7, "How do you handle authentication tokens that expire mid-suite?", [
        "Naive: fetch token in @BeforeSuite — breaks on long runs when token expires halfway.",
        "Better: TokenManager caches token + expiry; refresh on demand. Every request asks the manager.",
        "Thread safety: synchronize refresh so twenty threads do not all hit login simultaneously.",
        "Belt and braces: Filter that retries once on 401 after forcing a refresh (handles server-side revocation).",
    ]))

    story.append(qa(8, "What is your strategy for negative testing an API?", [
        "Systematic categories for every endpoint:",
        "• Missing required fields → 400 naming the field",
        "• Invalid data types",
        "• Boundary values — zero, negative, max, max+1, excessive decimals",
        "• Authorisation — no token, expired token, valid token for another customer's account (IDOR)",
        "• Non-existent resources → 404 not 500",
        "• Business rules — insufficient funds, frozen account, daily limits",
        "Assert the error contract, not just non-200. A vague 500 where 400 belongs is itself a defect.",
    ]))

    story.append(qa(9, "How do you integrate API tests into a CI/CD pipeline?", [
        "Tiered strategy: on every commit — smoke (&lt;2 min) fails the build; merge/nightly — full regression parallel; "
        "publish Allure as artifact.",
        "Practical: URLs/credentials from CI secrets; fail loudly (no silent skip); fix or quarantine flaky tests "
        "so the suite stays trustworthy.",
    ]))

    story.append(qa(10, "How do you decide what to test at the API layer versus the UI layer?", [
        "Test pyramid: API carries bulk of functional coverage (logic, validation, boundaries, authZ, contracts). "
        "UI: critical journeys, form display, navigation — small high-value E2E set.",
        "Anti-pattern: thirty validation permutations through the browser. One UI test proves wiring; API proves logic.",
    ]))

    story.append(qa(11, "BEHAVIOURAL: Automated tests missed a production bug.", [
        "Use STAR. Strong pattern: tests asserted HTTP status but not business outcome/state — silent failure until users reported.",
        "What changed: state-verification (re-read balance), schema validation, regression test for that defect. "
        "Lesson: assert on the state change, not merely the response.",
    ]))

    story.append(qa(12, "BEHAVIOURAL: Disagreed with a developer about a defect.", [
        "Bring data (request, response, spec clause), seek understanding, frame user/business impact. "
        "Strong close: ambiguous spec clarified, or you were wrong and adjusted the test. Graceful concession reads senior.",
    ]))

    story.append(qa(13, "BEHAVIOURAL: Flaky suite the team stopped trusting.", [
        "Measure first (which tests, how often). Triage root cause — shared data, races, env, real intermittent bugs. "
        "Quarantine out of blocking pipeline with time-boxed fix commitment. "
        "A suite nobody trusts provides negative value.",
    ]))

    story.append(qa(14, "How do you validate an API contract has not broken between releases?", [
        "• JSON schema on critical responses (needs json-schema-validator dependency)",
        "• Contract tests vs OpenAPI/Swagger, ideally generated from it",
        "• Consumer-driven contracts (Pact) in microservices so provider changes don't break unaware consumers",
        "Banking APIs feed mobile, partners and internal services — field type drift breaks consumers silently.",
    ]))

    story.append(qa(15, "Most common mistakes in API automation frameworks?", [
        "• Asserting only status codes",
        "• Hardcoded IDs/data",
        "• Endpoint URLs scattered (no service layer)",
        "• Hand-escaped JSON strings instead of POJOs",
        "• Order-dependent tests (kills parallel)",
        "• No negative coverage",
        "• Credentials committed to repo",
        "• Blanket retries masking real intermittent defects",
    ]))

    story.append(qa(16, "Show GPath filter and aggregate data in a response.", [
        "Favourite senior question. Banking uses: sum debits, find highest txn, confirm ownership.",
        code('float total = js.getFloat("sum{ it.amount }");\n'
             'List<Integer> overdrawn =\n'
             '    js.getList("findAll { it.balance < 0 }.id");\n'
             'float max = js.getFloat("max{ it.amount }.amount");\n'
             'int savings = js.getList("findAll { it.type == \'SAVINGS\' }").size();\n'
             '.then().body("findAll { it.balance < 0 }.size()", equalTo(2));'),
    ]))

    story.append(qa(17, "BANKING: Why should monetary values never be handled as double?", [
        "Floating-point cannot represent most decimal fractions exactly. 0.1 + 0.2 ≠ 0.3 in binary float. "
        "Production banking uses BigDecimal with explicit scale and rounding. Tests should mirror that.",
        code('// Fragile\n'
             'Assert.assertTrue(after == before - 100.00);\n'
             '// Acceptable delta\n'
             'Assert.assertEquals(after, before - 100.00, 0.001);\n'
             '// Best\n'
             'BigDecimal expected = before.subtract(new BigDecimal("100.00"));\n'
             'Assert.assertEquals(0, after.compareTo(expected));\n'
             '// compareTo, not equals — equals also compares scale (100.0 != 100.00)'),
    ]))

    story.append(qa(18, "BANKING: How do you test an asynchronous payment (202 + callback)?", [
        "Assert 202 + tracking reference; poll status until terminal state with timeout (Awaitility), never fixed sleep; "
        "for webhooks stand up a listener; assert terminal state and resulting balance change.",
        "Trap: asserting 202 alone only proves the request was queued.",
        code('Awaitility.await()\n'
             '    .atMost(30, TimeUnit.SECONDS)\n'
             '    .pollInterval(2, TimeUnit.SECONDS)\n'
             '    .until(() -> paymentService.getStatus(txnRef).equals("SETTLED"));\n'
             'Assert.assertEquals(0, accountService.getBalance(id)\n'
             '        .compareTo(expectedAfterSettlement));'),
    ]))

    story.append(qa(19, "How do you validate the database alongside the API?", [
        "API says what the service claims; DB confirms what was persisted (cache, incomplete txn, async write).",
        "Worth doing for financial transactions, audit trails, fields not in API response. Caveats: couples tests "
        "to schema; use read-only credentials; supplements API assertion, does not replace it.",
        code('String sql =\n'
             '  "SELECT amount, type FROM transaction " +\n'
             '  "WHERE account_id = ? ORDER BY date DESC LIMIT 1";\n'
             'try (PreparedStatement ps = conn.prepareStatement(sql)) {\n'
             '    ps.setInt(1, fromAccountId);\n'
             '    ResultSet rs = ps.executeQuery();\n'
             '    Assert.assertTrue(rs.next(), "No ledger entry written");\n'
             '    Assert.assertEquals(rs.getBigDecimal("amount")\n'
             '            .compareTo(new BigDecimal("100.00")), 0);\n'
             '}'),
    ]))

    story.append(qa(20, "BANKING: Full request/response logging is a compliance problem — how fix?", [
        "Payloads contain PII/sensitive data (account numbers, SSN, cards, tokens). Logging them writes that data "
        "into CI logs and report artifacts — a data-protection issue, not just untidy code.",
        "Fix: MaskingFilter redacts sensitive fields; prefer log().ifValidationFails(); never log Authorization raw.",
        code('public class MaskingFilter implements Filter {\n'
             '    private static final List<String> SENSITIVE =\n'
             '        List.of("ssn", "password", "cardNumber", "cvv", "token");\n'
             '    public Response filter(FilterableRequestSpecification req,\n'
             '                           FilterableResponseSpecification res,\n'
             '                           FilterContext ctx) {\n'
             '        Response response = ctx.next(req, res);\n'
             '        log.info(mask(response.asString()));\n'
             '        return response;\n'
             '    }\n'
             '}'),
    ]))

    story.append(qa(21, "What are REST Assured filters and what would you use them for?", [
        "A filter intercepts every request/response — API equivalent of a TestNG listener.",
        "Uses: inject auth token; structured/PII-masked logging; Allure attach; correlation IDs for server-side "
        "debug; retry once on 401 after token refresh.",
        code('RestAssured.filters(\n'
             '    new AllureRestAssured(),\n'
             '    new MaskingFilter(),\n'
             '    new CorrelationIdFilter()\n'
             ');'),
    ]))

    story.append(qa(22, "How do you handle third-party dependencies you cannot control?", [
        "Payment gateway / credit bureau / SMS: cost, rate-limits, hard to force failures. "
        "Service virtualisation (WireMock) stubs controlled responses for timeouts, declines, 503.",
        "Trade-off: mocks can drift — keep a small periodic sandbox contract suite against the real provider.",
        code('stubFor(post(urlEqualTo("/gateway/charge"))\n'
             '    .willReturn(aResponse()\n'
             '        .withStatus(503)\n'
             '        .withFixedDelay(5000)));'),
    ]))

    story.append(qa(23, "How do you test pagination, and what defects does it hide?", [
        "First/middle/last page; page size 0, 1, max, max+1; page past end → empty not 500; "
        "total count consistency; no duplicates/gaps across boundaries (classic unstable sort defect); "
        "concurrent insert while paging can silently drop items.",
    ]))

    story.append(qa(24, "How would you organise several hundred API tests?", [
        "Packages by domain (accounts, transfers, billpay); TestNG groups (smoke, regression, negative, contract); "
        "suite files (smoke.xml / regression.xml); naming method_condition_expectedResult; full independence.",
        "Someone should find the right test from a failure name alone and run any subset in parallel.",
    ]))

    story.append(qa(25, "How do you manage configuration and secrets across environments?", [
        "Env-specific properties (config-qa) selected by -Denv=qa; never commit credentials; ConfigReader fails "
        "loudly on missing keys; production (if any) strictly read-only by structure.",
        code('mvn test -Denv=qa -Dsuite=smoke\n'
             'String pwd = System.getenv("API_TEST_PASSWORD");'),
        tip("A repo with a committed password is a security incident."),
    ]))

    story.append(qa(26, "How do you integrate API tests with Allure reporting?", [
        "allure-rest-assured filter attaches request/response automatically. Use @Epic/@Feature/@Severity/@Story/@Step. "
        "Pair with MaskingFilter so attached payloads are redacted.",
        code('@Epic("Banking Core")\n'
             '@Feature("Fund Transfer")\n'
             '@Severity(SeverityLevel.BLOCKER)\n'
             'public class TransferApiTest extends BaseApiTest {\n'
             '  @Test(description = "Balances update correctly after transfer")\n'
             '  public void transfer_validAmount_updatesBothBalances() { ... }\n'
             '}'),
    ]))

    story.append(qa(27, "BEHAVIOURAL: Deliver testing under an unrealistic deadline.", [
        "Prioritise by risk; automate highest-value paths first; write down what is not covered so shipping is an "
        "informed decision. Then backfill debt. Avoid hero narrative of testing everything silently.",
    ]))

    story.append(qa(28, "BEHAVIOURAL: Production incident where testing was questioned.", [
        "Blameless analysis: impact, containment, why tests missed it (data gap, mock drift, env). "
        "Systemic fix: regression test + class-of-gap improvement (contract, negative, parity). No defensiveness.",
    ]))

    story.append(qa(29, "What would you improve about your current framework if you had more time?", [
        "Never answer 'nothing'. Credible options: OpenAPI contract tests; on-demand data factory; "
        "containerised deps for isolation; baselined performance assertions; mutation testing of assertions. "
        "Pick one you can discuss in depth.",
    ]))

    story.append(Spacer(1, 4))
    story.append(P("RAPID FIRE — one-liners", "DH2"))
    story.append(hline())
    story.append(rf(1, "Which is faster — API or UI automation?",
                    "API, roughly an order of magnitude. No browser, no rendering, no element waits."))
    story.append(rf(2, "Is PUT idempotent? Is POST?",
                    "PUT yes, POST no. Repeating POST /transfer could move money twice."))
    story.append(rf(3, "Difference between 401 and 403?",
                    "401 — not authenticated. 403 — authenticated but not permitted."))
    story.append(rf(4, "What does .extract() do?",
                    "Bridges validation to usage — must assign result to a variable."))
    story.append(rf(5, "What does @DataProvider give you?",
                    "TestNG data-driven testing — one method, many data sets."))
    story.append(rf(6, "Serialization vs deserialization?",
                    "Ser: Java → JSON request. Deser: JSON response → Java object."))
    story.append(rf(7, "Why use spec builders?",
                    "Common setup once and reused — API equivalent of BasePage. Parallel-safer than static baseURI."))
    story.append(rf(8, "What does JSON schema catch that value asserts miss?",
                    "Structural contract breaks — field removed/renamed/type-changed even with 200."))
    story.append(rf(9, "Why never money as double?",
                    "Float cannot represent decimals exactly; use BigDecimal + compareTo."))
    story.append(rf(10, "What does GPath findAll do?",
                   "Filters a collection: findAll { it.balance &lt; 0 } → overdrawn accounts."))
    story.append(rf(11, "What does 202 Accepted mean — testing trap?",
                   "Queued, not completed. Asserting 202 alone does not prove settlement."))
    story.append(rf(12, "What is a REST Assured filter?",
                   "Interceptor on every request/response — auth, logging, PII mask, reporting."))
    story.append(rf(13, "Why is logging full bodies risky in banking?",
                   "PII (SSN, card data) leaks into CI logs and report artifacts."))
    story.append(rf(14, "BigDecimal equals vs compareTo?",
                   "equals also compares scale (100.0 ≠ 100.00); compareTo returns 0 as expected."))
    story.append(rf(15, "What is WireMock used for?",
                   "Stub third parties so timeouts/declines/outages can be tested on demand."))
    story.append(rf(16, "Classic pagination defect?",
                   "Duplicates or gaps across page boundaries from unstable sort order."))
    story.append(rf(17, "Idempotency-Key purpose?",
                   "Same key + same body → one side-effect; protects retries of POST payments."))
    story.append(rf(18, "TokenManager under parallel?",
                   "Cache token + expiry; synchronize refresh; optional 401-retry filter."))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PART 3 — PRACTICE TESTS
    # ═══════════════════════════════════════════════════════
    story.append(P("PART 3 — Practice Tests", "DH1"))
    story.append(P("5 tests × 10 questions · increasing difficulty · answer without looking up, then check key", "LvlM"))
    story.append(hline())

    story.append(P("Practice Test 1 — Fundamentals (Easy)", "DH2"))
    story.append(mcq(1, "Which HTTP method retrieves data without changing server state?",
                     ["A) POST", "B) GET", "C) PUT", "D) DELETE"]))
    story.append(mcq(2, "What does status code 201 indicate?",
                     ["A) Request succeeded", "B) Resource created successfully", "C) Bad request", "D) Unauthorized"]))
    story.append(mcq(3, "In given/when/then, where is the HTTP method specified?",
                     ["A) In given()", "B) In .body()", "C) In .when().get(...)", "D) In .then()"]))
    story.append(mcq(4, "Which block contains request headers and body?",
                     ["A) given()", "B) when()", "C) then()", "D) extract()"]))
    story.append(mcq(5, "BANKING: Fetch customer account balance should use:",
                     ["A) POST", "B) GET", "C) PUT", "D) PATCH"]))
    story.append(mcq(6, "js.getList(\"$\").size() on an 11-element array prints:",
                     ["A) 11", "B) 10", "C) 0", "D) Compilation error"]))
    story.append(mcq(7, "Which status means client is not authenticated?",
                     ["A) 400", "B) 401", "C) 403", "D) 404"]))
    story.append(mcq(8, "Default format when ContentType.JSON is set?",
                     ["A) XML", "B) JSON", "C) HTML", "D) Plain text"]))
    story.append(mcq(9, "BANKING: Fund transfer creating a new transaction should use:",
                     ["A) GET", "B) POST", "C) HEAD", "D) OPTIONS"]))
    story.append(mcq(10, "response.jsonPath().getInt(\"[0].id\") extracts:",
                     ["A) Whole response", "B) First account's id", "C) All account ids", "D) Array size"]))

    story.append(Spacer(1, 4))
    story.append(P("Practice Test 2 — Core Concepts (Easy)", "DH2"))
    story.append(mcq(1, "Which annotation runs once before all tests in the suite?",
                     ["A) @BeforeMethod", "B) @BeforeClass", "C) @BeforeSuite", "D) @BeforeTest"]))
    story.append(mcq(2, "Purpose of .log().all() after then()?",
                     ["A) Logs the request", "B) Logs the response", "C) Logs both", "D) Disables logging"]))
    story.append(mcq(3, "Hamcrest matcher for field is not null?",
                     ["A) isNotNull()", "B) notNullValue()", "C) hasValue()", "D) exists()"]))
    story.append(mcq(4, "What is wrong: .get(\"GET /customers/12212/accounts\")?",
                     ["A) Missing then()", "B) HTTP verb is inside the URL string", "C) queryParam misspelled", "D) Nothing"]))
    story.append(mcq(5, "A path parameter is used to:",
                     ["A) Filter results", "B) Identify a specific resource in the URL", "C) Set content type", "D) Authenticate"]))
    story.append(mcq(6, "BANKING: Correct assertion for savings account type?",
                     ["A) assertEquals(type)", "B) .body(\"type\", equalTo(\"SAVINGS\"))", "C) .body(\"SAVINGS\")", "D) .type(\"SAVINGS\")"]))
    story.append(mcq(7, "List&lt;Integer&gt; ids = response.jsonPath().getList(\"id\"); does what?",
                     ["A) Prints all types", "B) Puts every element's id into a List", "C) Returns array size", "D) Throws"]))
    story.append(mcq(8, "Which status family is server-side error?",
                     ["A) 2xx", "B) 3xx", "C) 4xx", "D) 5xx"]))
    story.append(mcq(9, "BANKING: 200 OK + body status FAILED; test asserts only status code →",
                     ["A) Test fails correctly", "B) Test passes incorrectly", "C) Errors out", "D) RA auto-detects"]))
    story.append(mcq(10, "What must you do with .extract().response().asString() result?",
                     ["A) Nothing, prints automatically", "B) Assign it to a variable to use it", "C) Pass to then()", "D) Call .log()"]))

    story.append(PageBreak())
    story.append(P("Practice Test 3 — Framework Level (Medium)", "DH2"))
    story.append(mcq(1, "Which feature bundles base URI, headers and content type for reuse?",
                     ["A) ResponseSpecification", "B) RequestSpecBuilder", "C) JsonPath", "D) Filter"]))
    story.append(mcq(2, "matchesJsonSchemaInClasspath(...) achieves:",
                     ["A) Validates values", "B) Validates structure and data types", "C) Logs schema", "D) Serializes"]))
    story.append(mcq(3, "BANKING: To properly verify fund transfer moved money:",
                     ["A) Status 200 only", "B) Body says SUCCESS only",
                      "C) Read balances before/after and assert exact deltas", "D) Check endpoint is fast"]))
    story.append(mcq(4, "Correct way to send a POJO as JSON body?",
                     ["A) .body(pojo.toString())", "B) .body(pojo)", "C) .jsonBody(pojo)", "D) .serialize(pojo)"]))
    story.append(mcq(5, "In parallel execution, why is RestAssured.baseURI risky?",
                     ["A) Slower", "B) Global mutable state shared across threads", "C) No HTTPS", "D) Cannot read config"]))
    story.append(mcq(6, "Account a = response.as(Account.class); produces:",
                     ["A) JSON string", "B) Typed Account object with getters", "C) JsonPath", "D) Map"]))
    story.append(mcq(7, "GPath findAll { it.balance &lt; 0 }.id returns:",
                     ["A) Total balance", "B) Ids of all overdrawn accounts", "C) Number of accounts", "D) First id"]))
    story.append(mcq(8, "BANKING: Assert balance 1000 fails intermittently — most likely:",
                     ["A) Network latency", "B) Another test mutating the same shared account", "C) Wrong status", "D) Missing content-type"]))
    story.append(mcq(9, "Primary advantage of a service/endpoint layer?",
                     ["A) Faster execution", "B) Endpoint URLs live in one place", "C) Auto retries", "D) Built-in reporting"]))
    story.append(mcq(10, "Which assertion validates response time?",
                     ["A) .responseTime(2000)", "B) .time(lessThan(2000L))", "C) .duration(2000)", "D) .timeout(2000)"]))

    story.append(Spacer(1, 4))
    story.append(P("Practice Test 4 — Design &amp; Strategy (Medium)", "DH2"))
    story.append(mcq(1, "What does .log().ifValidationFails() provide over .log().all()?",
                     ["A) More detail", "B) Logs only when assertion fails (cleaner CI)", "C) Faster", "D) Logs to file"]))
    story.append(mcq(2, "BANKING: Customer A cannot access customer B's account tests for:",
                     ["A) Performance", "B) IDOR / authorisation flaw", "C) Schema compliance", "D) Idempotency"]))
    story.append(mcq(3, "@BeforeSuite fetchAuthToken() problem in long suite?",
                     ["A) Syntax error", "B) Token may expire mid-suite", "C) Too slow", "D) Cannot reuse"]))
    story.append(mcq(4, "TestNG config for methods parallel across 5 threads?",
                     ["A) parallel=\"tests\" thread-count=\"5\"", "B) parallel=\"methods\" thread-count=\"5\"",
                      "C) parallel=\"true\" threads=\"5\"", "D) concurrent=\"5\""]))
    story.append(mcq(5, "Field changes number→string but still 200. What catches this?",
                     ["A) Status assertion", "B) Response time", "C) JSON schema validation", "D) Logging"]))
    story.append(mcq(6, "BANKING: MOST important negative for transfer API?",
                     ["A) Valid amount", "B) Insufficient funds", "C) Fetch balance", "D) Login success"]))
    story.append(mcq(7, "BANKING: Logging full bodies with SSN/cards is primarily:",
                     ["A) Performance problem", "B) Data-protection/compliance breach", "C) Formatting", "D) OK in test envs"]))
    story.append(mcq(8, "Test third-party gateway timeout best approach?",
                     ["A) Wait for real outage", "B) WireMock delayed 503", "C) Skip", "D) Increase own timeout"]))
    story.append(mcq(9, "Capture accountId then GET /accounts/{id}/transactions demonstrates:",
                     ["A) Serialization", "B) Chaining — value feeds next request", "C) Schema", "D) Parallel"]))
    story.append(mcq(10, "Strongest test data strategy for shared banking env?",
                     ["A) Hardcoded IDs", "B) Fixed seed shared by all", "C) Each test creates and owns data", "D) IDs from text file"]))

    story.append(Spacer(1, 4))
    story.append(P("Practice Test 5 — Real-World Scenarios (Hard)", "DH2"))
    story.append(mcq(1, "20 threads all refresh expired token at once — best fix?",
                     ["A) Increase token lifetime", "B) Synchronise refresh so only one fetches", "C) Disable parallel", "D) Retry thrice"]))
    story.append(mcq(2, "BANKING: Network retry double-moves money. Prevention?",
                     ["A) Rate limiting", "B) Idempotency keys on the request", "C) Schema validation", "D) Response time"]))
    story.append(mcq(3, "Defect in: Assert.assertTrue(after == before - 100.00)?",
                     ["A) Syntax", "B) Floating-point comparison without delta/BigDecimal", "C) Wrong method", "D) Missing status"]))
    story.append(mcq(4, "Provider change breaks three unaware consumers. Which practice catches it?",
                     ["A) Higher UI coverage", "B) Consumer-driven contracts (Pact)", "C) Longer timeouts", "D) More threads"]))
    story.append(mcq(5, "Transfer passes alone, fails in parallel — MOST likely?",
                     ["A) Insufficient threads", "B) Tests share account and mutate balance", "C) Slow network", "D) Wrong base URI"]))
    story.append(mcq(6, "200 + SUCCESS + time&lt;2s but still incomplete — missing?",
                     ["A) Status code", "B) Money actually moved — no state re-read", "C) Content-Type", "D) Response time"]))
    story.append(mcq(7, "BigDecimal(\"100.00\").equals(BigDecimal(\"100.0\")) fails because:",
                     ["A) Wrong method name", "B) equals also compares scale", "C) Cannot compare BigDecimal", "D) Delta missing"]))
    story.append(mcq(8, "Strongest guarantee bill payment succeeded?",
                     ["A) 200 only", "B) 200 + body status",
                      "C) 200 + body status + source balance decrease + matching ledger entry", "D) Time under 2s"]))
    story.append(mcq(9, "202 Accepted asserted alone — missing?",
                     ["A) Response time", "B) Confirmation payment reached terminal settled state", "C) Content-Type", "D) Schema"]))
    story.append(mcq(10, "Suite fails randomly ~15%; team ignores failures. FIRST action?",
                     ["A) Add retries everywhere", "B) Delete flaky tests",
                      "C) Measure which tests fail intermittently and why", "D) Increase all waits"]))

    story.append(PageBreak())

    # ── ANSWER KEY ─────────────────────────────────────────
    story.append(P("Answer Key — All five practice tests", "DH1"))
    story.append(hline())

    story.append(P("Practice Test 1 — Fundamentals (Easy)", "DH2"))
    story.append(mini_table(
        ["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"],
        [["1", "B", "2", "B", "3", "C", "4", "A", "5", "B"],
         ["6", "A", "7", "B", "8", "B", "9", "B", "10", "B"]],
        [0.45*inch, 0.55*inch] * 5
    ))
    story.append(Spacer(1, 6))

    story.append(P("Practice Test 2 — Core Concepts (Easy)", "DH2"))
    story.append(mini_table(
        ["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"],
        [["1", "C", "2", "B", "3", "B", "4", "B", "5", "B"],
         ["6", "B", "7", "B", "8", "D", "9", "B", "10", "B"]],
        [0.45*inch, 0.55*inch] * 5
    ))
    story.append(Spacer(1, 6))

    story.append(P("Practice Test 3 — Framework Level (Medium)", "DH2"))
    story.append(mini_table(
        ["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"],
        [["1", "B", "2", "B", "3", "C", "4", "B", "5", "B"],
         ["6", "B", "7", "B", "8", "B", "9", "B", "10", "B"]],
        [0.45*inch, 0.55*inch] * 5
    ))
    story.append(Spacer(1, 6))

    story.append(P("Practice Test 4 — Design &amp; Strategy (Medium)", "DH2"))
    story.append(mini_table(
        ["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"],
        [["1", "B", "2", "B", "3", "B", "4", "B", "5", "C"],
         ["6", "B", "7", "B", "8", "B", "9", "B", "10", "C"]],
        [0.45*inch, 0.55*inch] * 5
    ))
    story.append(Spacer(1, 6))

    story.append(P("Practice Test 5 — Real-World Scenarios (Hard)", "DH2"))
    story.append(mini_table(
        ["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"],
        [["1", "B", "2", "B", "3", "B", "4", "B", "5", "B"],
         ["6", "B", "7", "B", "8", "C", "9", "B", "10", "C"]],
        [0.45*inch, 0.55*inch] * 5
    ))

    story.append(Spacer(1, 10))
    story.append(hline())
    story.append(P("60-second pitch", "DH2"))
    story.append(P(
        "“I build Rest Assured + TestNG suites with env config, reusable RequestSpecifications, service clients, "
        "POJO payloads (BigDecimal for money), TokenManager with safe refresh, schema checks on critical contracts, "
        "data-driven regression, Allure/CI parallel runs with isolated data. Assertions cover HTTP and business status "
        "plus state re-read; sensitive fields are redacted in logs.”",
        "DTip"
    ))
    story.append(P("Must-practice snippets", "DH2"))
    story.append(P(
        "1) GET + status + body &nbsp; 2) POST POJO + extract id &nbsp; 3) Bearer/oauth2 &nbsp; 4) path+query params &nbsp; "
        "5) RequestSpec reuse &nbsp; 6) GPath findAll/sum &nbsp; 7) Schema validation &nbsp; 8) create→get→delete cleanup &nbsp; "
        "9) Transfer balance delta (BigDecimal) &nbsp; 10) Idempotency-Key + MaskingFilter",
        "DBody"
    ))
    story.append(P(
        "Interview mindset: syntax gets you past screening; banking risk language (idempotency, IDOR, PII, "
        "double-debit, async settlement) wins senior rounds.",
        "DFix"
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.45 * inch,
        title="REST Assured API Automation — SDET Interview Q&A",
        author="Interview Prep (verified)",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote: {OUT}")
    print(f"Size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    build()
