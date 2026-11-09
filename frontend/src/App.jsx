import { useEffect, useState } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import UploadBox from "./components/UploadBox";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

import API from "./services/api";

function App() {
  const [loading, setLoading] = useState(false);

  const [activeChats, setActiveChats] = useState([]);
  const [archivedChats, setArchivedChats] = useState([]);

  const [activeChatId, setActiveChatId] = useState(null);

  const refreshChats = async () => {
  try {
    const response = await API.get("/chats");

    console.log("CHAT DATA:");
    console.log(response.data);

    setActiveChats(response.data.active || []);
    setArchivedChats(response.data.archived || []);

    if (
      response.data.active?.length > 0 &&
      !activeChatId
    ) {
      setActiveChatId(
        response.data.active[0].id
      );
    }

  } catch (err) {
    console.error(err);
  }
};

  useEffect(() => {
    refreshChats();
  }, []);

  const createNewChat = async () => {
    try {
      await API.post("/chat/create");

      await refreshChats();
    } catch (err) {
      console.error(err);
    }
  };

  const archiveChat = async (chatId) => {
    try {
      await API.post(
        `/chat/${chatId}/archive`
      );

      await refreshChats();
    } catch (err) {
      console.error(err);
    }
  };

  const deleteChat = async (
    chatId,
    archived = false
  ) => {
    try {
      await API.delete(
        `/chat/${chatId}`,
        {
          params: {
            archived,
          },
        }
      );

      await refreshChats();
    } catch (err) {
      console.error(err);
    }
  };




  const activeChat =
    activeChats.find(
      (c) => c.id === activeChatId
    );

  const unarchiveChat = async (chatId) => {

  try {

    await API.post(
      `/chat/${chatId}/unarchive`
    );

    await refreshChats();

  }

  catch (err) {

    console.error(err);

  }

};

  return (
    <div className="app">
      <Sidebar
  activeChats={activeChats}
  archivedChats={archivedChats}
  activeChatId={activeChatId}
  setActiveChatId={setActiveChatId}
  createNewChat={createNewChat}
  refreshChats={refreshChats}
  archiveChat={archiveChat}
  unarchiveChat={unarchiveChat}
  deleteChat={deleteChat}
/>

      <div className="main-content">
        <UploadBox />

        <ChatWindow
          messages={
            activeChat?.messages || []
          }
          loading={loading}
        />

        {activeChat && (
          <ChatInput
            chats={activeChats}
            setChats={setActiveChats}
            activeChatId={activeChatId}
            setLoading={setLoading}
          />
        )}
      </div>
    </div>
  );
}

export default App;