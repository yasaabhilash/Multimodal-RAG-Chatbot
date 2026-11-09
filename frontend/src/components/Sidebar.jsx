import API from "../services/api";

function Sidebar({
  activeChats,
  archivedChats,
  activeChatId,
  setActiveChatId,
  createNewChat,
  refreshChats,
  archiveChat,
  unarchiveChat,
  deleteChat
}) {

  const renameChat = async (chat) => {

    const newTitle = prompt(
      "Enter new chat name",
      chat.title
    );

    if (!newTitle) return;

    try {

      await API.put(
        `/chat/${chat.id}/rename`,
        {
          title: newTitle
        }
      );

      refreshChats();

    } catch (err) {

      console.error(err);

    }

  };

  return (

    <div className="sidebar">

      <button
        className="new-chat"
        onClick={createNewChat}
      >
        + New Chat
      </button>

      <h3 style={{ marginTop: "20px" }}>
        Chats
      </h3>

      {activeChats?.map((chat) => (

        <div
          key={chat.id}
          className={
            activeChatId === chat.id
              ? "history-item active-chat"
              : "history-item"
          }
        >

          <div
            onClick={() =>
              setActiveChatId(chat.id)
            }
          >
            {chat.title}
          </div>

          <div
            style={{
              marginTop: "5px"
            }}
          >

            <button
              onClick={() =>
                renameChat(chat)
              }
            >
              Rename
            </button>

            <button
              onClick={() =>
                archiveChat(chat.id)
              }
            >
              Archive
            </button>

          </div>

        </div>

      ))}

      <h3 style={{ marginTop: "20px" }}>
        Archived
      </h3>

      {archivedChats?.map((chat) => (

  <div
    key={chat.id}
    className="history-item"
  >

    {chat.title}

    <br />

    <button
      onClick={() =>
        unarchiveChat(chat.id)
      }
    >
      Unarchive
    </button>

    <button
      onClick={() =>
        deleteChat(
          chat.id,
          true
        )
      }
    >
      Delete
    </button>

  </div>

))}

    </div>

  );

}

export default Sidebar;