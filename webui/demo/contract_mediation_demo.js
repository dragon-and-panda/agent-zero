const bidBtn = document.getElementById("attach-bid-btn");
const sendEmailBtn = document.getElementById("send-email-btn");
const bidToast = document.getElementById("bid-toast-anchor");
const emailStatus = document.getElementById("email-status");

if (bidBtn && bidToast) {
  bidBtn.addEventListener("click", () => {
    const proposalUri = document.getElementById("bid-uri")?.value?.trim() || "inline-line-items";
    bidToast.textContent = `Bid attached successfully (${proposalUri}). Neutral AI is summarizing line items.`;
    bidToast.style.color = "var(--accent)";
  });
}

if (sendEmailBtn && emailStatus) {
  sendEmailBtn.addEventListener("click", () => {
    const now = new Date().toLocaleTimeString();
    emailStatus.textContent = `Progress email marked sent at ${now}.`;
    emailStatus.style.color = "var(--accent)";
  });
}
