export function getTimeZone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

export function getTimeOffset() {
    return new Date().getTimezoneOffset();
}