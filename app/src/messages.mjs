export function prepareMessages(messages) {
  return messages
    .map((message) => ({
      role: message.role,
      text: message.content
        .filter((part) => part.type === "text")
        .map((part) => part.text)
        .join("\n"),
    }))
    .filter(
      (message) =>
        message.role !== "assistant" || message.text.trim().length > 0,
    );
}
export function retryLatestUser(thread) {
  const user = thread
    .getState()
    .messages.findLast((message) => message.role === "user");
  if (!user) throw new Error("請先填寫問題。");
  return thread.startRun({ parentId: user.id });
}
