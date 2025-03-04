import { Box } from "@mui/material";
import { FC, useEffect, useRef, useState } from "react";
import { useAppDispatch, useAppSelector } from "./app/hooks";
import Body from "./Body/Body";
import Header from "./Header/Header";
import { LogContainerKeys, selectLogFiltersState, selectSideBarState } from "./redux/containerInfoSlice";
import SideBarContainer from "./Sidebar/SidebarContainer";
import mqtt, { MqttClient } from "mqtt";
import { incrementContainerLogCount, selectContainerLogCount } from "./redux/exhibitScreensSlice";
import { format } from "util";

export type Log = {
  type: "docker" | "console";
  message: string;
  containerName: LogContainerKeys;
};

const Main: FC = () => {
  const isSideBarOpen = useAppSelector(selectSideBarState);
  const containerLogCounts = useAppSelector(selectContainerLogCount);
  const filterState = useAppSelector(selectLogFiltersState)
  const dispatch = useAppDispatch();
  const [sideBarWidth, setSideBarWidth] = useState("35%");
  const [logs, setLogs] = useState<Log[]>([]);
  const isSideBarOpenRef = useRef(isSideBarOpen);
  const filterStateRef = useRef(filterState);

  useEffect(() => {
    isSideBarOpenRef.current = isSideBarOpen;
  }, [isSideBarOpen]);

  useEffect(() => {
    filterStateRef.current = filterState;
  }, [filterState]);

  useEffect(() => {
    const handleResize = () => {
      if(window.innerWidth * 0.35 < 750){
        setSideBarWidth("35%");
      }else{
        setSideBarWidth("750px");
      }
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    const mqttClient = mqtt.connect("ws://localhost:9001", {
      clientId: "mqtt-logger-ui",
    });

    const originalLog = console.log;

    console.log = function(...args) {
      const message = format(...args);
      mqttClient.publish('app/logs/single-screen-development', message);
      originalLog.apply(console, args);
    };

    mqttClient.on("connect", () => {
      console.log("Connected to MQTT broker");
      mqttClient.subscribe("docker/logs/#", (err) => {
        if (!err) {
          console.log("Subscribed to docker/logs/");
        } else {
          console.error("Failed to subscribe:", err);
        }
      });
      mqttClient.subscribe("app/logs/#", (err) => {
        if (!err) {
          console.log("Subscribed to app/logs/");
        } else {
          console.error("Failed to subscribe:", err);
        }
      });
    });

    mqttClient.on("message", (topic, message) => {
      const containerName = topic.split("/").pop() as LogContainerKeys;
      let type : "docker" | "console";
      if (topic.includes("docker/logs/")) {
        type = "docker"
      } else if (topic.includes("app/logs/")) {
        type = "console";
      }
      if(containerLogCounts[containerName] !== undefined){
        console.log("IS IT OPEN: " + isSideBarOpenRef.current)
        if(isSideBarOpenRef.current === false){
          console.log('here :' + type! + " " + containerName)
          dispatch(incrementContainerLogCount(containerName));
        }else{
          console.log('here2 :' + type! + " " + containerName)
          if(!filterStateRef.current.logType[type!] || !filterStateRef.current.containers[containerName]){
            dispatch(incrementContainerLogCount(containerName));
          }
        }
      }
      setLogs(prev => [...prev, {type: type, message: message.toString(),containerName: containerName! }])
    });

    mqttClient.on("error", (err) => {
      console.error("MQTT error:", err);
    });

    return () => {
      if (mqttClient) {
        mqttClient.end(); // Disconnect the client
      }
    };
  }, []);

  return (
    <>
      <SideBarContainer sideBarWidth={sideBarWidth} logs={logs}></SideBarContainer>
      <Box
        className="App"
        sx={{
          display: "flex",
          flexGrow: 1,
          flexDirection: "column",
          backgroundColor: "#1E1E1E",
          height: "100vh",
          width: `${isSideBarOpen ? `calc(100vw - ${sideBarWidth})` : "100vw"}`,
          alignItems: "center",
          padding: `${isSideBarOpen ? `0px 25px` : "0px 90px"}`,
          marginLeft: `${isSideBarOpen ? `${sideBarWidth}` : "0px"}`,
          transition: 'all 0.3s ease'
        }}
      >
        <Header></Header>
        <Body></Body>
      </Box>
    </>
  );
};
export default Main;
