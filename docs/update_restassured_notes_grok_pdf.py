"""Rebuild RestAssured_Interview_Questions_Notes_grok.pdf with accuracy polish.

Original: Rahul Shetty course + advanced senior gaps (38 Qs + killer answers).
Polish: specs vs static baseURI, schema dependency, preemptive basic, TokenManager
ThreadLocal, HTTP vs business status, BigDecimal money note, PII filters, 429/idempotency.
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted
)

OUT = Path(
    r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material"
    r"\CLAUDE AI NOTES\REST ASSURED API AUTOAMTION NOTES"
    r"\RestAssured_Interview_Questions_Notes_grok.pdf"
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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14,
                          leading=17, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=8.5,
                          leading=11, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
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
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=BLUE, spaceAfter=1))
styles.add(ParagraphStyle(name="LvlM", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=TEAL, spaceAfter=1))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=RED, spaceAfter=1))
styles.add(ParagraphStyle(name="DBullet", fontName="Helvetica", fontSize=7.5,
                          leading=9.6, textColor=DARK, leftIndent=6, spaceAfter=1))


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


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12, A4[0], 12, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 6.3)
        canvas.drawString(26, A4[1] - 8, "Rest Assured Interview Notes | Grok Updated")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "Easy · Medium · Difficult")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.3)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Rest Assured API Automation", "TMain")],
        [P("Interview Questions &amp; Notes — Updated Edition<br/>"
           "Based on Rahul Shetty Udemy course + real interview gaps<br/><br/>"
           "EASY Fundamentals &nbsp;·&nbsp; MEDIUM Framework &nbsp;·&nbsp; DIFFICULT Senior / Real-World<br/>"
           "38 Q&amp;A + Bonus killer answers",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 26))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Original notes already covered course core + senior gaps (filters, Jackson, token expiry, polling, "
        "pagination, 429, parallel). Verified and lightly polished for interview accuracy.",
        "DBody"
    ))
    story.append(polish(
        "RequestSpec over static baseURI; preemptive basic auth; json-schema-validator dependency; "
        "TokenManager + ThreadLocal; HTTP 200 vs business status; Idempotency-Key; 429 Retry-After; "
        "PII/token log redaction; money note (BigDecimal)."
    ))
    story.append(P(
        "How to use: answer first, then read. Practice every snippet in IDE. For “tell me about your framework”, "
        "draw layers then walk Ecommerce E2E + token expiry + parallel.",
        "DBody"
    ))
    story.append(PageBreak())

    # ── EASY ───────────────────────────────────────────────
    story.append(P("1. EASY LEVEL — Must-know Fundamentals", "DH1"))
    story.append(P("REST basics, Rest Assured syntax, extractors, matchers", "LvlB"))
    story.append(hline())

    story.append(qa(1, "What is a REST API?", [
        "REST (Representational State Transfer) is an architectural style that uses standard HTTP methods on "
        "resources identified by URIs. It is stateless, cacheable, and commonly uses JSON (or XML) as the representation.",
    ]))

    story.append(qa(2, "Difference between REST and SOAP?", [
        "• <b>REST</b> → lightweight, HTTP verbs, JSON preferred, flexible contract, better performance for most modern APIs.",
        "• <b>SOAP</b> → XML only, WSDL contract, heavier, formal security/transactions (still common in legacy banking cores).",
    ]))

    story.append(qa(3, "HTTP Methods and when to use them", [
        "• <b>GET</b> → Retrieve (safe + idempotent)",
        "• <b>POST</b> → Create / action (not idempotent — retry can double side-effects)",
        "• <b>PUT</b> → Full replace (idempotent)",
        "• <b>PATCH</b> → Partial update",
        "• <b>DELETE</b> → Remove (idempotent by design)",
        tip("Banking: retried POST /transfer can move money twice → use Idempotency-Key."),
    ]))

    story.append(qa(4, "Important HTTP Status Codes", [
        "• <b>2xx:</b> 200 OK · 201 Created · 202 Accepted (queued) · 204 No Content",
        "• <b>4xx:</b> 400 Bad Request · 401 Unauthorized · 403 Forbidden · 404 Not Found · 405 · 409 · 422 · 429 Too Many Requests",
        "• <b>5xx:</b> 500 · 502 · 503 · 504",
        tip("401 = not authenticated; 403 = authenticated but not allowed."),
    ]))

    story.append(qa(5, "What is Rest Assured?", [
        "A Java DSL library (built on Apache HTTP Client) with fluent given/when/then syntax for readable REST tests. "
        "Supports JSON/XML, auth helpers, schema modules, serialization, logging, and TestNG/JUnit integration.",
    ]))

    story.append(qa(6, "Basic Rest Assured syntax (given-when-then)", [
        code('given()\n'
             '    .queryParam("key", "qaclick123")\n'
             '    .header("Content-Type", "application/json")\n'
             '.when()\n'
             '    .get("https://rahulshettyacademy.com/maps/api/place/get/json")\n'
             '.then()\n'
             '    .assertThat().statusCode(200)\n'
             '    .body("status", equalTo("OK"));'),
        polish("In frameworks, put base URI/headers in RequestSpecification — avoid hardcoding full URLs in every test."),
    ]))

    story.append(qa(7, "How do you extract values from a response?", [
        "1. JsonPath: js.getString(\"access_token\")",
        "2. Response path: response.jsonPath().get(\"courses[0].title\")",
        "3. POJO deserialization (preferred for complex responses) → type-safe and reusable.",
        "Always assign .extract() results to a variable — discarding silently is a common bug.",
        code('Response r = given().spec(req).when().get("/courses")\n'
             '    .then().statusCode(200).extract().response();\n'
             'String title = r.jsonPath().getString("courses[0].title");'),
    ]))

    story.append(qa(8, "Path Parameter vs Query Parameter", [
        "• <b>Path:</b> part of resource URL → /users/{userId} → .pathParam(\"userId\", 123)",
        "• <b>Query:</b> after ? → /users?status=active → .queryParam(\"status\", \"active\")",
        "Path identifies which resource; query filters or supplies action inputs.",
    ]))

    story.append(qa(9, "Common Hamcrest matchers you must know", [
        "equalTo, hasItem, hasItems, hasSize, containsString, notNullValue, greaterThan, lessThan, "
        "everyItem, hasKey, empty, not, startsWith.",
        tip("Pin one Hamcrest version if TestNG + Rest Assured clash (NoSuchMethodError)."),
    ]))

    story.append(qa(10, "How do you validate response time?", [
        code('.then().time(lessThan(2000L));  // milliseconds'),
        "Lightweight smoke SLA only — not a substitute for load testing (JMeter/Gatling). "
        "Use env-specific thresholds (UAT can be slower without being a product bug).",
    ]))

    story.append(qa(11, "How do you send form-urlencoded data?", [
        "Used heavily for OAuth token endpoints.",
        code('.contentType("application/x-www-form-urlencoded")\n'
             '.formParam("client_id", clientId)\n'
             '.formParam("client_secret", clientSecret)\n'
             '.formParam("grant_type", "client_credentials")\n'
             '.when().post("/oauth/token");'),
        tip("Never commit client_secret — inject from env / CI secrets."),
    ]))

    story.append(PageBreak())

    # ── MEDIUM ─────────────────────────────────────────────
    story.append(P("2. MEDIUM LEVEL — Framework Thinking", "DH1"))
    story.append(P("POJO, specs, auth, schema, filters, Jackson, soft asserts", "LvlM"))
    story.append(hline())

    story.append(qa(12, "What is Serialization &amp; Deserialization?", [
        "• <b>Serialization</b> → Java object → JSON (request body)",
        "• <b>Deserialization</b> → JSON → Java object (response)",
        "Course style: Jackson + POJO classes (GetCourse, Api, Courses, Mobile…). Preferred over pure JsonPath for maintainability.",
        "Needs Jackson (or Gson) on the classpath.",
    ]))

    story.append(qa(13, "Why use POJO classes instead of JsonPath everywhere?", [
        "Type safety · readability · reuse · IDE completion · cleaner assertions · refactor-friendly. "
        "JsonPath typos fail only at runtime; POJO typos fail at compile time.",
        polish("For money fields in banking APIs, prefer BigDecimal over double/float in POJOs."),
    ]))

    story.append(qa(14, "RequestSpecification &amp; ResponseSpecification", [
        "Building blocks of a real framework (DRY). Never repeat base URI, headers, content-type, expected status.",
        code('RequestSpecification req = new RequestSpecBuilder()\n'
             '    .setBaseUri(ConfigReader.get("base.uri"))\n'
             '    .addQueryParam("key", ConfigReader.get("api.key"))\n'
             '    .setContentType(ContentType.JSON)\n'
             '    .addFilter(new MaskingFilter())\n'
             '    .build();\n'
             'ResponseSpecification res = new ResponseSpecBuilder()\n'
             '    .expectStatusCode(200)\n'
             '    .expectContentType(ContentType.JSON)\n'
             '    .build();\n'
             'given().spec(req).when().get("/endpoint").then().spec(res);'),
        polish("Prefer specs over RestAssured.baseURI statics — safer under parallel execution."),
    ]))

    story.append(qa(15, "How do you handle dynamic payloads?", [
        "• HashMap / POJO + setters at runtime",
        "• External JSON + string substitution (careful with escaping)",
        "• TestNG @DataProvider / Excel / JSON files",
        "• Java Faker / UUID for unique test data (critical for parallel)",
    ]))

    story.append(qa(16, "Authentication types you must know", [
        "• Basic Auth — .auth().basic(user, pass)",
        "• Preemptive Basic — .auth().preemptive().basic(...) (sends credentials before 401 challenge)",
        "• Digest Auth",
        "• OAuth 1.0 / 2.0 (Client Credentials heavily used in the course)",
        "• Bearer / JWT — .auth().oauth2(token) or Authorization header",
        "• API Key — header or query param",
        "Never hard-code tokens; generate at runtime and inject via spec/filter.",
    ]))

    story.append(qa(17, "How do you validate JSON Schema?", [
        polish("Requires dependency: io.rest-assured:json-schema-validator (not on rest-assured alone)."),
        code('.then().assertThat()\n'
             '    .body(matchesJsonSchemaInClasspath("schemas/schema.json"));'),
        "Keep schema files under src/test/resources. Catches field removed/renamed/type-changed even when status is still 200.",
    ]))

    story.append(qa(18, "Logging in Rest Assured", [
        code('.log().all()                 // request or response depending on position\n'
             '.log().ifError()             // only on HTTP error\n'
             '.log().ifValidationFails()   // only when assertion fails (best for CI)\n'
             '.log().body()                // body only'),
        tip("In banking/fintech, mask tokens/PII — never dump Authorization or SSN raw into CI/Allure."),
    ]))

    story.append(qa(19, "Filters in Rest Assured (very important)", [
        "• Built-in: RequestLoggingFilter, ResponseLoggingFilter",
        "• Custom filters: correlation IDs, mask tokens/passwords, attach to Allure, inject Bearer, retry once on 401",
        "Almost every production framework uses custom filters — API equivalent of TestNG listeners.",
        code('RestAssured.filters(\n'
             '    new AllureRestAssured(),\n'
             '    new MaskingFilter(),\n'
             '    new CorrelationIdFilter()\n'
             ');'),
    ]))

    story.append(qa(20, "Jackson annotations every interviewer expects", [
        "• @JsonIgnore — skip a field",
        "• @JsonProperty(\"actual_key\") — map different JSON key names",
        "• @JsonInclude(JsonInclude.Include.NON_NULL) — omit nulls when serializing",
        "• @JsonIgnoreProperties(ignoreUnknown = true) — ignore extra response fields (API adds fields without breaking tests)",
    ]))

    story.append(qa(21, "Soft Assertions", [
        "Hard assert stops on first failure. Soft assert (TestNG SoftAssert or AssertJ) continues and reports all "
        "failures together. Critical for E2E flows where you want a full picture of what broke.",
        code('SoftAssert soft = new SoftAssert();\n'
             'soft.assertEquals(status, "OK");\n'
             'soft.assertNotNull(orderId);\n'
             'soft.assertAll();  // report all'),
    ]))

    story.append(qa(22, "How do you handle cookies / sessions?", [
        "Extract cookie from response → reuse with .cookie() or .cookies() on the next request. "
        "Can also use a cookie filter. Session-based APIs (some banking UIs under the hood) need careful parallel isolation.",
    ]))

    story.append(qa(23, "Environment management (QA / Stage / Prod)", [
        "Use config.properties (or YAML) + Maven profiles / system properties (-Denv=qa). "
        "Never hard-code baseURI or credentials. Same suite runs against any env by changing only config.",
        "Secrets from System.getenv / CI secret store. Fail loudly if a required key is missing. "
        "If anything touches production: structurally force read-only.",
        code('mvn test -Denv=qa -Dsuite=smoke'),
    ]))

    story.append(PageBreak())

    # ── DIFFICULT ──────────────────────────────────────────
    story.append(P("3. DIFFICULT / REAL-WORLD — Senior Level", "DH1"))
    story.append(P("E2E, OAuth, TokenManager, async, parallel, security", "LvlR"))
    story.append(hline())

    story.append(qa(24, "End-to-End Ecommerce flow (course Section 13)", [
        "Typical design question: Login → Get Token → Create Product → Create Order → Get Order Details → Delete Order.",
        "Talk about: TokenManager (ThreadLocal preferred under parallel), response chaining (extract IDs), SoftAssert, "
        "cleanup in @AfterMethod even on failure, logging every step, unique data so runs don’t collide.",
    ]))

    story.append(qa(25, "OAuth 2.0 Client Credentials Grant", [
        "1. Hit token endpoint with client_id + client_secret (form-urlencoded)",
        "2. Extract access_token",
        "3. Pass as Bearer on subsequent calls",
        "4. Handle expiry with TokenManager + refresh logic",
        "Never hard-code tokens; always generate at runtime from secrets.",
    ]))

    story.append(qa(26, "How do you design a scalable Rest Assured framework?", [
        "Layered architecture:",
        "• <b>base</b> → BaseApiTest (filters, optional SSL config)",
        "• <b>specs</b> → Request/Response SpecBuilders",
        "• <b>pojos</b> → request/response models",
        "• <b>services</b> → endpoint methods (no raw URLs in tests)",
        "• <b>utils</b> → TokenManager, ConfigReader, JsonUtils, poller, RetryAnalyzer",
        "• <b>tests</b> → feature classes (smoke/regression groups)",
        "• <b>listeners/reports</b> → Extent/Allure",
        "Also: multi-env config, parallel + isolated data, CI/CD, schema on critical contracts.",
    ]))

    story.append(qa(27, "Token expiry mid-suite (very common senior question)", [
        "Access tokens often expire in 30–60 min. Long suites die mid-way if token is only fetched in @BeforeSuite.",
        "Solution: TokenManager stores token + expiry timestamp. Before every request (or via filter), check validity; "
        "if expired, refresh. Use ThreadLocal (or synchronized manager) so parallel threads don’t thrash login.",
        "Belt-and-braces: filter retries once on 401 after forced refresh (handles server-side revocation).",
    ]))

    story.append(qa(28, "Polling / Async APIs", [
        "API returns 202 Accepted. Poll status endpoint until COMPLETED/FAILED with max attempts + interval. "
        "Never infinite loops or fixed long sleeps only.",
        code('// Prefer Awaitility-style poller\n'
             'Awaitility.await()\n'
             '    .atMost(30, TimeUnit.SECONDS)\n'
             '    .pollInterval(2, TimeUnit.SECONDS)\n'
             '    .until(() -> orderService.status(id).equals("COMPLETED"));'),
        tip("Asserting 202 alone only proves the request was queued — always verify terminal state + side-effect."),
    ]))

    story.append(qa(29, "Pagination testing", [
        "Loop next page (page/size or next-link) until last page. Validate total count; no duplicates/gaps across "
        "pages (classic unstable sort defect). Edge: page size 0/1/max, page past end → empty not 500.",
    ]))

    story.append(qa(30, "Idempotency testing", [
        "Prove calling the same POST/PUT multiple times does not create duplicates. Send same Idempotency-Key "
        "(or unique business key); assert one resource / one ledger entry / one balance delta.",
        code('given().spec(req)\n'
             '  .header("Idempotency-Key", key)\n'
             '  .body(payload)\n'
             '.when().post("/payments")\n'
             '.then().statusCode(201);\n'
             '// same key + body again → same payment id, not a second charge'),
    ]))

    story.append(qa(31, "Rate limiting (429) handling", [
        "Detect 429 → read Retry-After if present (else exponential backoff) → limited retries. "
        "Never hammer the server in CI. Log retries clearly. Tune TestNG thread-count so the suite itself doesn’t cause 429s.",
    ]))

    story.append(qa(32, "How do you handle SSL / certificate issues?", [
        code('// Dev/QA self-signed only — config-driven, never unconditional in prod-facing runs\n'
             'if (cfg.relaxedSsl()) {\n'
             '    RestAssured.useRelaxedHTTPSValidation();\n'
             '}'),
        "Production-grade: import server cert into Java truststore; don’t disable verification permanently.",
    ]))

    story.append(qa(33, "Mutual TLS / Client Certificate authentication", [
        "Beyond relaxedHTTPSValidation. Configure Rest Assured / HTTP client with a keystore (client cert) and "
        "truststore. Common in banking and high-security partner APIs. Keep certs/passwords out of git.",
    ]))

    story.append(qa(34, "File upload / download", [
        "• Upload: .multiPart(\"file\", new File(\"path\")) (+ extra form fields as multiPart)",
        "• Download: response.asByteArray() or write stream to File; assert Content-Type and size/hash if relevant",
    ]))

    story.append(qa(35, "Parallel execution pitfalls &amp; ThreadLocal", [
        "Shared static token or shared test data causes race conditions and flaky balance assertions.",
        "Solution: ThreadLocal for tokens (or thread-safe TokenManager), unique data (Faker + UUID), own fixtures per "
        "test, careful cleanup. Prefer RequestSpec instances over mutating RestAssured statics. Design for parallel from day one.",
    ]))

    story.append(qa(36, "How do you properly test DELETE?", [
        "Status 204/200 is not enough. After DELETE, GET the same resource and assert 404 (gone). "
        "Also verify related resources if the API has cascading deletes.",
    ]))

    story.append(qa(37, "Real production problems interviewers love", [
        "• API returns 200 but business logic failed → always validate body + application status + state re-read",
        "• Contract testing mindset (schema / OpenAPI / Pact) even if tool adoption is partial",
        "• API versioning in automation (/v1/, /v2/, header-based)",
        "• Same suite against QA/Stage/Prod via config only",
        "• Masking secrets (tokens, passwords, PII) in logs and Allure/Extent via custom filters",
    ]))

    story.append(qa(38, "Security-oriented questions (growing trend)", [
        "• <b>BOLA / IDOR:</b> valid token for user A must not read/update user B’s resource (expect 403/404)",
        "• <b>Mass assignment / excessive data exposure:</b> extra fields in body ignored; response doesn’t leak admin-only fields",
        "• <b>Sensitive data in reports:</b> MaskingFilter redacts before attach; never log Authorization raw",
        "• Broken auth: no token, expired token, wrong role",
    ]))

    story.append(Spacer(1, 6))
    story.append(P("BONUS — Killer answers that impress interviewers", "DH2"))
    story.append(hline())
    for line in [
        "I always keep Request and Response specs in a separate class and reuse them.",
        "I never hard-code tokens — TokenManager with expiry check + ThreadLocal under parallel.",
        "I use Allure + custom Rest Assured filters so every request/response is attached and secrets are masked.",
        "For dynamic data I prefer POJO + Java Faker over Excel in modern frameworks.",
        "Adding a new endpoint needs a new POJO + service method + thin test — not 50 copy-paste URLs.",
        "Critical flows run in parallel with TestNG; state is isolated per thread.",
        "I always verify DELETE with a subsequent GET expecting 404.",
        "I have a reusable poller for async APIs with timeout and interval (not infinite sleep).",
        "HTTP 200 is not enough — I assert business status and re-read state (balance/order).",
        "Payment retries use Idempotency-Key so double-submit cannot double-charge.",
    ]:
        story.append(P(f"• “{line}”", "DBullet"))

    story.append(Spacer(1, 6))
    story.append(P("Final tip — whiteboard story", "DH2"))
    story.append(P(
        "When the interviewer says “Tell me about your framework”, draw the layered architecture, then walk "
        "Ecommerce (or banking transfer) E2E: login → token → create → get → delete/cleanup, and explicitly cover "
        "token expiry, parallel isolation, and how you avoid false greens on HTTP 200 + business FAILED.",
        "DBody"
    ))
    story.append(P("60-second pitch", "DH2"))
    story.append(P(
        "“I build Rest Assured + TestNG suites with env config, reusable specs, service clients, POJOs, "
        "TokenManager with safe refresh, schema on critical contracts, data-driven tests, Allure with masked logs, "
        "and parallel runs with unique data. Assertions cover HTTP, business status, and state side-effects.”",
        "DTip"
    ))
    story.append(P("Must-practice snippets", "DH2"))
    story.append(P(
        "1) given/when/then GET &nbsp; 2) form-urlencoded OAuth token &nbsp; 3) Bearer header &nbsp; 4) RequestSpec/ResponseSpec &nbsp; "
        "5) POJO ser/deser &nbsp; 6) extract chain create→get→delete &nbsp; 7) schema validation &nbsp; 8) SoftAssert E2E &nbsp; "
        "9) poller for 202 &nbsp; 10) MaskingFilter + Idempotency-Key",
        "DBody"
    ))

    # Cross-ref note
    story.append(Spacer(1, 4))
    story.append(P(
        "Related deeper bank: RestAssured_API_Interview_QA_claude.pdf (fundamentals + senior banking + 50 MCQs). "
        "Related compact Q&amp;A: Rest_Assured_Interview_Questions_Answers_grokbuild.pdf.",
        "DFix"
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.45 * inch,
        title="Rest Assured Interview Questions & Notes (Grok Updated)",
        author="Interview Prep (verified)",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote: {OUT}")
    print(f"Size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    build()
