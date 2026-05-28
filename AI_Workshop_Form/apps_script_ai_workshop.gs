/**
 * AI Agent Workshop intake endpoint.
 *
 * Deployment target:
 * Google Apps Script > Deploy > New deployment > Web app
 * Execute as: Me
 * Who has access: Anyone with the link
 *
 * Frontend should POST application/x-www-form-urlencoded with a `payload`
 * field containing JSON. This avoids browser CORS preflight issues with
 * Apps Script web apps.
 */

const CONFIG = {
  SHEET_ID: '1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64',
  RESPONSES_TAB: 'AIWorkshopResponses',
  INSTRUCTOR_EMAIL: 'vuhoang2708@gmail.com',
  EMAIL_SENDER_NAME: 'AI Agent Workshop',
};

const RESPONSE_HEADERS = [
  'timestamp',
  'submissionId',
  'source',
  'fullName',
  'email',
  'phoneZalo',
  'roleTeam',
  'sessionPreference',
  'joinMode',
  'aiTools',
  'aiToolsOther',
  'aiUseCases',
  'aiUseCasesOther',
  'satisfaction',
  'frustrations',
  'expectation',
  'concreteTask',
  'budgetRange',
  'preferredOutput',
  'consentEmail',
  'status',
  'rawPayloadJson',
];

function doPost(e) {
  try {
    const payload = parsePayload_(e);
    return json_(handleWorkshopIntake_(payload));
  } catch (err) {
    return json_({
      ok: false,
      error: err && err.message ? err.message : String(err),
    });
  }
}

function doGet() {
  return json_({
    ok: true,
    service: 'AI Agent Workshop intake endpoint',
    sheetId: CONFIG.SHEET_ID,
    responsesTab: CONFIG.RESPONSES_TAB,
  });
}

function handleWorkshopIntake_(payload) {
  if (clean_(payload.website)) {
    return {
      ok: true,
      skipped: true,
      message: 'Submission ignored.',
    };
  }

  requireFields_(payload, [
    'fullName',
    'email',
    'roleTeam',
    'sessionPreference',
    'expectation',
    'concreteTask',
    'consentEmail',
  ]);
  validateEmail_(payload.email);

  if (String(payload.consentEmail) !== 'yes') {
    throw new Error('Cần đồng ý nhận email xác nhận/tài liệu để gửi form.');
  }

  const timestamp = new Date();
  const submissionId = clean_(payload.submissionId) || makeSubmissionId_('aiw');
  const sheet = getSheet_(CONFIG.RESPONSES_TAB, RESPONSE_HEADERS);

  sheet.appendRow([
    timestamp,
    submissionId,
    clean_(payload.source || 'ai_workshop_form'),
    clean_(payload.fullName),
    clean_(payload.email),
    clean_(payload.phoneZalo),
    clean_(payload.roleTeam),
    clean_(payload.sessionPreference),
    clean_(payload.joinMode),
    normalizeList_(payload.aiTools),
    clean_(payload.aiToolsOther),
    normalizeList_(payload.aiUseCases),
    clean_(payload.aiUseCasesOther),
    clean_(payload.satisfaction),
    clean_(payload.frustrations),
    clean_(payload.expectation),
    clean_(payload.concreteTask),
    clean_(payload.budgetRange),
    clean_(payload.preferredOutput),
    clean_(payload.consentEmail),
    'new',
    stringifyJson_(payload),
  ]);

  sendInstructorEmail_(payload, submissionId, timestamp);
  sendParticipantEmail_(payload, submissionId);

  return {
    ok: true,
    kind: 'ai_workshop_intake',
    submissionId,
    message: 'Thông tin đã được ghi vào Google Sheet và email xác nhận đã được gửi.',
  };
}

function sendInstructorEmail_(payload, submissionId, timestamp) {
  const subject = `[AI Workshop] Form mới - ${clean_(payload.fullName)}`;
  const body = [
    'Có phản hồi mới từ form AI Agent Workshop.',
    '',
    `Submission ID: ${submissionId}`,
    `Thời gian: ${timestamp}`,
    `Họ tên: ${clean_(payload.fullName)}`,
    `Email: ${clean_(payload.email)}`,
    `SĐT/Zalo: ${clean_(payload.phoneZalo)}`,
    `Vai trò/team: ${clean_(payload.roleTeam)}`,
    `Hình thức tham gia: ${clean_(payload.joinMode)}`,
    `Lịch mong muốn: ${clean_(payload.sessionPreference)}`,
    '',
    'Cách đang dùng AI:',
    `- Công cụ: ${normalizeList_(payload.aiTools)} ${clean_(payload.aiToolsOther)}`,
    `- Use case: ${normalizeList_(payload.aiUseCases)} ${clean_(payload.aiUseCasesOther)}`,
    `- Điều đang hài lòng: ${clean_(payload.satisfaction)}`,
    `- Điều gây khó chịu / mất thời gian: ${clean_(payload.frustrations)}`,
    '',
    'Kỳ vọng và bài toán thật:',
    `- Kỳ vọng: ${clean_(payload.expectation)}`,
    `- Bài toán mang tới workshop: ${clean_(payload.concreteTask)}`,
    `- Budget phù hợp: ${clean_(payload.budgetRange)}`,
    `- Output mong muốn: ${clean_(payload.preferredOutput)}`,
    '',
    'CTA cho người hướng dẫn: đọc dòng mới trong tab AIWorkshopResponses, gom nhóm use case, chuẩn bị demo theo bài toán thật của người tham gia.',
  ].join('\n');

  sendEmail_(CONFIG.INSTRUCTOR_EMAIL, subject, body, {
    replyTo: clean_(payload.email),
    name: CONFIG.EMAIL_SENDER_NAME,
  });
}

function sendParticipantEmail_(payload, submissionId) {
  const subject = 'Xác nhận đã nhận thông tin đăng ký AI Agent Workshop';
  const body = [
    `Chào ${clean_(payload.fullName)},`,
    '',
    'Mình đã nhận thông tin của bạn cho buổi AI Agent Workshop.',
    '',
    'Tóm tắt thông tin đã ghi nhận:',
    `- Vai trò/team: ${clean_(payload.roleTeam)}`,
    `- Lịch mong muốn: ${clean_(payload.sessionPreference)}`,
    `- Hình thức tham gia: ${clean_(payload.joinMode)}`,
    `- Công cụ AI đang dùng: ${normalizeList_(payload.aiTools)} ${clean_(payload.aiToolsOther)}`,
    `- Bài toán muốn mang tới workshop: ${clean_(payload.concreteTask)}`,
    `- Mã phản hồi: ${submissionId}`,
    '',
    'Trước buổi chia sẻ, bạn có thể chuẩn bị một ví dụ thật: prompt đã dùng, output AI trả về, và chỗ bạn thấy chưa đúng ý. Như vậy phần demo sẽ sát việc thật hơn.',
    '',
    'Trân trọng,',
    'AI Agent Workshop',
  ].join('\n');

  sendEmail_(clean_(payload.email), subject, body, {
    name: CONFIG.EMAIL_SENDER_NAME,
  });
}

function getSheet_(tabName, headers) {
  const spreadsheet = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  let sheet = spreadsheet.getSheetByName(tabName);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(tabName);
  }

  ensureHeaders_(sheet, headers);
  return sheet;
}

function ensureHeaders_(sheet, headers) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    return;
  }

  const width = Math.max(sheet.getLastColumn(), headers.length);
  const existing = sheet.getRange(1, 1, 1, width).getValues()[0].map(clean_);
  const expected = headers.map(clean_);
  const headMismatch = existing.slice(0, expected.length).join('\u0001') !== expected.join('\u0001');
  const extraHeaders = existing.slice(expected.length).some(Boolean);

  if (headMismatch || extraHeaders) {
    sheet.getRange(1, 1, 1, width).clearContent();
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }
}

function parsePayload_(e) {
  if (!e || !e.postData) {
    throw new Error('Missing POST body.');
  }

  const raw = e.postData.contents || '';
  const type = e.postData.type || '';

  if (e.parameter && e.parameter.payload) {
    return JSON.parse(e.parameter.payload);
  }

  if (type.indexOf('application/json') !== -1 || raw.trim().charAt(0) === '{') {
    return JSON.parse(raw);
  }

  const data = {};
  Object.keys(e.parameter || {}).forEach((key) => {
    data[key] = e.parameter[key];
  });
  return data;
}

function requireFields_(payload, fields) {
  const missing = fields.filter((field) => !clean_(payload[field]));
  if (missing.length) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }
}

function validateEmail_(email) {
  const value = clean_(email);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    throw new Error('Invalid email.');
  }
}

function sendEmail_(to, subject, body, options) {
  MailApp.sendEmail(to, subject, body, options || {});
}

function clean_(value) {
  return String(value == null ? '' : value).trim();
}

function normalizeList_(value) {
  if (Array.isArray(value)) {
    return value.map(clean_).filter(Boolean).join(', ');
  }
  return clean_(value);
}

function stringifyJson_(value) {
  return JSON.stringify(value || {});
}

function makeSubmissionId_(prefix) {
  return `${prefix}_${Utilities.getUuid()}`;
}

function json_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
