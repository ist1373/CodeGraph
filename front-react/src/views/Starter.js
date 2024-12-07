import { Col, Row, Input, Label,Button, Card, CardBody, CardTitle, CardText,ListGroup,ListGroupItem } from "reactstrap";
import React, { useCallback, useState, useRef } from 'react';
import SalesChart from "../components/dashboard/SalesChart";
import Feeds from "../components/dashboard/Feeds";
import ProjectTables from "../components/dashboard/ProjectTable";
import { Graphistry } from '@graphistry/client-api-react';
import Blog from "../components/dashboard/Blog";
import bg1 from "../assets/images/bg/bg1.jpg";
import bg2 from "../assets/images/bg/bg2.jpg";
import bg3 from "../assets/images/bg/bg3.jpg";
import bg4 from "../assets/images/bg/bg4.jpg";
import axios from "axios";
import { useEffect } from 'react';
import Prism from 'prismjs';
import "../assets/prism1.css";
require("prismjs/components/prism-python");

const IFRAME_STYLE = { height: '800px', width: '100%', border: 0 };
// const [selection, setSelection] = useState(undefined);
// const [inputSelection, setInputSelection] = useState('{ "point": [], "edge": [0] }');
// const [show, setShow] = useState(false);



const BlogData = [
  {
    image: bg1,
    title: "This is simple blog",
    subtitle: "2 comments, 1 Like",
    description:
    `    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = [i for i in arr[1:] if i <= pivot]
        greater = [i for i in arr[1:] if i > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)`,
    btnbg: "primary",
  },
  {
    image: bg2,
    title: "Lets be simple blog",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
  {
    image: bg3,
    title: "Don't Lamp blog",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
  {
    image: bg4,
    title: "Simple is beautiful",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
];

const Starter = () => {
  // const [selection, setSelection] = useState(undefined);
  const [inputSelection, setInputSelection] = useState('{ "point": [], "edge": [0] }');
  const graphistryRef = useRef();
  
  const [inputValue, setInputValue] = useState("");
  const [results, setResults] = useState([]);
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  useEffect(() => {
    Prism.highlightAll();
    }, [results]);


  // const formatText = (text) => {
  //   // Split the text by \n and map each part to a React Fragment with a <br /> tag
  //   return text.split("\n").map((line, index) => (
  //     <React.Fragment key={index}>
  //       {line}
  //       <br />
  //     </React.Fragment>
  //   ));
  // };


  const handleButtonClick = async () => {
    try {
      // Replace 'https://api.example.com/endpoint' with your API endpoint
      const response = await axios.get("http://localhost:8000/semantic-path-search", {
        params: { query: inputValue },
      });
      console.log("API Response:", response.data);

      if (response.data.results) {
        setResults(response.data.results);
      }

    } catch (error) {
      console.error("Error calling the API:", error);
    }
  };

// const [show, setShow] = useState(false);
  return (
    <div>
      {/***Top Cards***/}

      {/***Sales & Feed***/}
      <Row>
          <Graphistry dataset='0e23e627e8984324b44853fc92f44667' 
              iframeStyle={IFRAME_STYLE}
              graphistryHost='https://hub.graphistry.com'/>
      </Row>
      <Row>
        <Col sm="12" lg="12" xl="12" xxl="12">
          <Card>
            <CardBody>

            <CardTitle tag="h5" className=" p-2 mb-0">
              Search over the PKG:
            </CardTitle>
            

            <Input className="p-2 m-2 mb-3 " id="exampleText" name="text" type="textarea" onChange={handleInputChange}/>

            <div className="d-flex justify-content-end mb-3">
              <Button className="btn" color="primary" onClick={handleButtonClick}>
                  Search
              </Button>
            </div>
  
            {results.length > 0 && (
              <ListGroup>
                {results.map((item, index) => (
                  <ListGroupItem key={index} style={{ whiteSpace: "pre-wrap" }}>
                    {/* {item.content}  */}
                      <pre >
                        <code className={'language-python'}>{item.content}</code>
                      </pre>
                      {/* <CodeHighlighter code={item.content} language="python" /> */}
                    Similarity Score: {item.similarity}
                    </ListGroupItem>
                ))}
              </ListGroup>
              
            )}
            </CardBody>
          </Card>
        </Col>
      </Row>
      
      {/* <Row>
        <Col sm="6" lg="6" xl="7" xxl="8">
          <SalesChart />
        </Col>
        <Col sm="6" lg="6" xl="5" xxl="4">
          <Feeds />
          
        </Col>
      </Row> */}
      {/***Table ***/}
      {/***Blog Cards***/}
      {/* <Row>
        {BlogData.map((blg, index) => (
          <Col sm="6" lg="6" xl="3" key={index}>
            <Blog
              image={blg.image}
              title={blg.title}
              subtitle={blg.subtitle}
              text={blg.description}
              color={blg.btnbg}
            />
          </Col>
        ))}
      </Row> */}
    </div>
  );
};

export default Starter;
