import { Box } from "@mui/material";
import { FC } from "react";
import ExhibitScreen from "../Screen Grid/Screen/ExhibitScreen";

interface GameScreenProps {
  connectionString: string;
}

const GameScreen: FC<GameScreenProps> = ({
    connectionString
                                         }) => {
  return (
    <>
        {/*<div className="aspectwrapper">*/}
        {/*    <div className="content">*/}
        {/*        <Box*/}
        {/*            className="Body"*/}
        {/*            sx={{*/}
        {/*                height: "95%",*/}
        {/*                margin: "0 auto",*/}
        {/*                backgroundColor: "green",*/}
        {/*                boxShadow:*/}
        {/*                    "0px 20px 25px -5px rgba(0, 0, 0, 0.3), 0px 10px 10px -5px rgba(0, 0, 0, 0.2)",*/}
        {/*                aspectRatio: "16 / 9",*/}
        {/*            }}*/}
        {/*        >*/}
        {/*            <iframe src="http://localhost:5000" width="100%" height="100%">*/}
        {/*            </iframe>*/}
        {/*        </Box>*/}
        {/*    </div>*/}
        {/*</div>*/}

                    <iframe  className = "content" src={connectionString} width="1280 px" height="720 px">
                    </iframe>

    </>
  );
};

export default GameScreen;
