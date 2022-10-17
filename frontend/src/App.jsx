import { useState } from "react";
import reactLogo from "./assets/react.svg";
import logo from "./assets/loko.svg";
import "./App.css";
import {
  Box,
  Button,
  Center,
  Flex,
  HStack,
  Image,
  Input,
  Link,
  Stack,
} from "@chakra-ui/react";
import { Carousel } from "react-carousel-minimal";
import axios from "axios";
import urljoin from "url-join";
import { Page } from "./Page";
const baseURL = import.meta.env.VITE_BASE_URL || "/";

const captionStyle = {
  fontSize: "2em",
  fontWeight: "bold",
};
const slideNumberStyle = {
  fontSize: "15px",
  fontWeight: "bold",
  color: "#ff9900",
};

const IMAGES_TYPES = {
  SEGMENT: "/load_segment",
  SEARCH_BOX: "/load_searchBox",
};

const DELETE_TYPES = {
  DELETE_SEGMENT: "/delete_segment",
  DELETE_SEARCHBOX: "/delete_searchBox",
};

function App() {
  const [listImages, setListImages] = useState();
  const [selected, setSelected] = useState("");

  const fetchData = async (imagesType) => {
    const response = await axios
      .get(baseURL + imagesType)
      .catch((err) => console.log(err));
    const images = response.data;
    console.log(images);
    setListImages(images.map((el) => ({ image: urljoin(baseURL, el.image) })));
  };

  const deleteData = async (imagesType) => {
    const response = await axios
      .delete(baseURL + imagesType)
      .then((data) => setListImages([]))
      .catch((err) => console.log(err));
  };

  return (
    <Page>
      <Flex h="100%" m="0">
        <Stack w="20%" h="100%" bg="blue.200">
          <HStack
            p="0.5rem"
            w="100%"
            py="20px"
            bg="orange.200"
            align={"center"}
          >
            <Image src={logo} w="20px" h="30px" alt="LoKo Icon" />
            <Box>LOKO AI SEGMENTER</Box>
          </HStack>
          <Center
            as={Link}
            p="2rem"
            bg={selected === "segment" && "orange"}
            onClick={() => {
              setSelected("segment");
              fetchData(IMAGES_TYPES.SEGMENT);
            }}
            fontWeight="bold"
            borderRadius={"10px"}
          >
            SEGMENT
          </Center>
          <Center
            as={Link}
            p="2rem"
            bg={selected === "search" && "orange"}
            onClick={() => {
              setSelected("search");
              fetchData(IMAGES_TYPES.SEARCH_BOX);
            }}
            fontWeight="bold"
            borderRadius={"10px"}
          >
            SEARCH BOX
          </Center>
          <Center
            h= "325px"
            >
          </Center>
        </Stack>
        <Flex direction="column" w="90%" h="100%">
          <div style={{ textAlign: "center" }}>
            <div
              style={{
                padding: "0px",
              }}
            >
              {listImages && (
                <>
                  <Carousel
                    data={listImages}
                    time={8000}
                    width="100%"
                    height="500px"
                    captionStyle={captionStyle}
                    radius="10px"
                    slideNumber={true}
                    slideNumberStyle={slideNumberStyle}
                    captionPosition="bottom"
                    automatic={true}
                    dots={true}
                    pauseIconColor="white"
                    pauseIconSize="40px"
                    slideBackgroundColor="#4d4d4d"
                    slideImageFit="contain"
                    thumbnails={false}
                    thumbnailWidth="100px"
                    style={{
                      textAlign: "center",
                      width: "450px",
                      height: "450PX",
                      margin: "40px auto",
                    }}
                  />
                  <button
                    onClick={() => {
                      if (selected === "segment") {
                        deleteData(DELETE_TYPES.DELETE_SEGMENT);
                      }
                      if (selected === "search") {
                        deleteData(DELETE_TYPES.DELETE_SEARCHBOX);
                      }
                    }}
                    className="button-delete"
                  />
                </>
              )}
            </div>
          </div>
        </Flex>
      </Flex>
    </Page>
  );
}

export default App;
