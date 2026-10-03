// https://dev.to/bybydev/how-to-slugify-a-string-in-javascript-4o9n
function slugify(str) {
  str = str.replace(/^\s+|\s+$/g, ''); // trim leading/trailing white space
  str = str.toLowerCase(); // convert string to lowercase
  str = str.replace(/[^a-z0-9 -]/g, '') // remove any non-alphanumeric characters
           .replace(/\s+/g, '-') // replace spaces with hyphens
           .replace(/-+/g, '-'); // remove consecutive hyphens
  return str;
}
// https://stackoverflow.com/questions/36488176/how-to-get-first-2-words
function truncateToFirstWords(str, wordNum=2) {
  return str.split(' ').slice(0, wordNum).join(' ')
}


// https://www.perplexity.ai/search/6aa43ba9-634f-4528-b141-ab4eb16a8763
function formatDate(date) {
  return new Intl.DateTimeFormat("en-GB", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(date));
}

function timeSince(startDate, endDate = "") {
  const start = new Date(`${startDate}T00:00:00`);
  const end = endDate
    ? new Date(`${endDate}T00:00:00`)
    : new Date();

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    throw new Error("Invalid date");
  }

  if (end < start) {
    throw new Error("End date must be after start date");
  }

  let years = end.getFullYear() - start.getFullYear();
  let months = end.getMonth() - start.getMonth();
  let days = end.getDate() - start.getDate();

  if (days < 0) {
    months--;

    const daysInPreviousMonth = new Date(
      end.getFullYear(),
      end.getMonth(),
      0
    ).getDate();

    days += daysInPreviousMonth;
  }

  if (months < 0) {
    years--;
    months += 12;
  }

  const parts = [];

  if (years) parts.push(`${years} year${years === 1 ? "" : "s"}`);
  if (months) parts.push(`${months} month${months === 1 ? "" : "s"}`);
  if (days) parts.push(`${days} day${days === 1 ? "" : "s"}`);

  return parts.length ? parts.join(", ") : "0 days";
}

// Read a cookie value, used to get the CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
  }
  return cookieValue;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}