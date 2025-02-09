
function AddMessage(){
    var input = document.getElementById('MessageInput');
    var text = input.value;
    let xhr = new XMLHttpRequest();
    let url = "AddMessage";

    // open a connection
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('SendMessage()： received data:' + this.responseText);
            const history = JSON.parse(this.responseText);
            UpdateChatHistoryView(history);
        }
    };
    // Converting JSON data to string
    const data = JSON.stringify(
        {
            "UserName": G_UserName,
            "ChatRoomId": G_ChatRoomId,
            "Message": text
        });
    // Sending data with the request
    console.log('SendMessage()： sending data:'+data);
    xhr.send(data);
    input.value = "";
}
function GetChatHistory()
{
    let xhr = new XMLHttpRequest();
    let url = "GetHistory";

    // open a connection
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    // Converting JSON data to string
    const data = JSON.stringify({
        "ChatRoomId": G_ChatRoomId
    });
    // Sending data with the request
    console.log('GetChatHistory()： sending data:'+data);
    xhr.send(data);
    if (xhr.readyState === 4 && xhr.status === 200) {
        console.log('GetChatHistory()： received data:' + xhr.responseText);
        return JSON.parse(xhr.responseText);
    }
    return [];
}
var G_LastHistory = null;
function UpdateChatHistory()
{
    const history = GetChatHistory();
    if(G_LastHistory != null && G_LastHistory === history)
    {
        console.log('UpdateChatHistory(): chat history is same as last record, no need to update!');
        return;
    }
    G_LastHistory = history;
    UpdateChatHistoryView(history);
}
function GenMessagePageCode(userName, messages, time)
{
    var messagePageCode = "";
    if(messages.length > 0)
    {
        var messageCode = "";
        var msgStyle = messages.length>1?"multi-msg":"single-msg";
        for (const msg of messages) {
          messageCode += `<p class="${msgStyle}">${msg.trim()}</p>\n`;
        }
        const style = userName===G_UserName?'outgoing':'received';
        const image = userName===G_UserName?'user1.png':'user2.png';
        const displayName = userName===G_UserName?'&nbsp;&nbsp;You':userName;
        const divStype = userName===G_UserName?'outgoing-chats-msg':'received-msg-inbox';
        messagePageCode = `
        <div class="${style}-chats">
            <div class="${style}-chats-img"> <img src="image/${image}"> ${displayName}</div>
            <div class="${style}-msg">
              <div class="${divStype}">
                ${messageCode}
                <span class="time">${time} by ${userName}</span>
              </div>
            </div>
         </div>
        `;
    }
    return messagePageCode;
}
var G_LastChatHistoryViewCode = '';
function UpdateChatHistoryView(history)//history is a jsonfied list []
{
    //generate html code
    var chatHistoryViewCode = "";
    var lastUserName = "";
    var userMessageList = [];
    var lastMessageTime = "";
    for (const item of history) {
      if(item["SenderName"]!==lastUserName)
      {
          chatHistoryViewCode += GenMessagePageCode(lastUserName, userMessageList, lastMessageTime);
          userMessageList = [];
      }
      lastUserName = item['SenderName'];
      userMessageList.push(item['Content']);
      lastMessageTime = item['Time'];
    }
    if(userMessageList.length > 0)
    {
        chatHistoryViewCode += GenMessagePageCode(lastUserName, userMessageList, lastMessageTime);
    }
    if(chatHistoryViewCode === G_LastChatHistoryViewCode)
    {
        console.log("UpdateChatHistoryView(): chatHistoryViewCode is same as previous one, no need to update!");
        return;
    }
    G_LastChatHistoryViewCode = chatHistoryViewCode;
    //replace inner html content
    var messagePage = document.getElementById('MessagePage');
    messagePage.innerHTML = chatHistoryViewCode;
    messagePage.scrollTo({
        top: messagePage.scrollHeight,
        behavior: 'smooth'
    });
    console.log('UpdateChatHistoryView(): replace innerHTML of MessagePage with:\n'+chatHistoryViewCode);
}