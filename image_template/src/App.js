import { useState } from "react";
import * as React from "react";
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  CardHeader,
  Checkbox,
} from "@mui/material";

function getImagePaths(directory) {
  let images = [];
  directory.keys().map((item, index) => images.push(item.replace("./", "")));
  return images;
}

function App() {
  const lowResDirectory = require.context(
    "./assets/low-res",
    false,
    /\.(png|jpe?g|svg)$/
  );
  const originalDirectory = require.context(
    "./assets/original",
    false,
    /\.(png|jpe?g|svg)$/
  );
  const predictedDirectory = require.context(
    "./assets/predicted",
    false,
    /\.(png|jpe?g|svg)$/
  );

  let lowResImagePaths = getImagePaths(lowResDirectory);
  let lowResImages = [];
  lowResImagePaths.map((path) =>
    lowResImages.push(require("./assets/low-res/" + path))
  );

  let originalImagePaths = getImagePaths(originalDirectory);
  let originalImages = [];
  originalImagePaths.map((path) =>
    originalImages.push(require("./assets/original/" + path))
  );

  let predictedImagePaths = getImagePaths(predictedDirectory);
  let predictedImages = [];
  predictedImagePaths.map((path) =>
    predictedImages.push(require("./assets/predicted/" + path))
  );

  let finalSet = [];
  for (let i = 0; i < lowResImages.length; i++) {
    let imgObj = {
      low: lowResImages[i],
      og: originalImages[i],
      ai: predictedImages[i],
    };
    finalSet.push(imgObj);
  }
  console.log(finalSet);
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        width: "100%",
        height: "auto",
        backgroundColor: "#242424",
      }}
    >
      <Grid
        sx={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-evenly",
          width: "90%",
          height: "auto",
          background: "#242424",
          // paddingRight: 4,
          // my: 2,
        }}
        container
        spacing={4}
      >
        {finalSet.map((image, index) => {
          return (
            <>
              <Grid item xs={4} key={index}>
                <Card sx={{ width: 500, my: 3, background: "#3b3b3b" }}>
                  <CardHeader title="Low-Resolution" sx={{ color: "white" }} />
                  <CardMedia
                    component="img"
                    height="500"
                    image={image.low}
                    alt="CT-Scan Image"
                  />
                  <CardContent sx={{ height: "50px" }}></CardContent>
                </Card>
              </Grid>
              <Grid item xs={4} key={index}>
                <Card sx={{ width: 500, my: 3, background: "#3b3b3b" }}>
                  <CardHeader title="Option A" sx={{ color: "white" }} />
                  <CardMedia
                    component="img"
                    height="500"
                    image={image.og}
                    alt="CT-Scan Image"
                  />
                  <CardContent
                    sx={{
                      display: "flex",
                      justifyContent: "flex-start",
                      alignItems: "center",
                      height: "30%",
                    }}
                  >
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-around",
                        alignItems: "center",
                        width: "40%",
                        background: "#444544",
                        border: "3px solid #424242",
                      }}
                    >
                      <Typography variant="h6" color="white">
                        Option A
                      </Typography>
                      <Checkbox color="secondary" />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={4} key={index}>
                <Card sx={{ width: 500, my: 3, background: "#3b3b3b" }}>
                  <CardHeader title="Option B" sx={{ color: "white" }} />
                  <CardMedia
                    component="img"
                    height="500"
                    image={image.ai}
                    alt="CT-Scan Image"
                  />
                  <CardContent
                    sx={{
                      display: "flex",
                      justifyContent: "flex-start",
                      alignItems: "center",
                    }}
                  >
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-around",
                        alignItems: "center",
                        width: "40%",
                        background: "#444544",
                        border: "3px solid #424242",
                      }}
                    >
                      <Typography variant="h6" color="white">
                        Option B
                      </Typography>
                      <Checkbox color="secondary" />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </>
          );
        })}
      </Grid>
    </Box>
  );
}
export default App;
