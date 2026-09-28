import { useState } from "react";

function ResultCard({ data }) {
  // Total revenue
  if (
    data &&
    data.total_revenue !== undefined &&
    data.status === undefined
  ) {
    return (
      <div className="result-card">
        <div className="result-label">Total Revenue</div>

        <div className="result-value">
          ₹{Number(data.total_revenue).toLocaleString("en-IN")}
        </div>
      </div>
    );
  }

  // Monthly revenue
  if (Array.isArray(data)) {
    return (
      <div className="result-card">
        <div className="result-label">Monthly Revenue</div>

        <div className="data-table">
          <div className="table-row table-header">
            <span>Month</span>
            <span>Revenue</span>
          </div>

          {data.map((row, index) => (
            <div className="table-row" key={index}>
              <span>{row.month}</span>

              <span>
                ₹{Number(row.revenue).toLocaleString("en-IN")}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Knowledge / RAG
  if (data && data.answer !== undefined) {
    return (
      <div className="result-card knowledge-card">
        <div className="result-label">Knowledge</div>

        <div className="knowledge-answer">
          {data.answer}
        </div>

        {data.sources && data.sources.length > 0 && (
          <div className="sources">
            <div className="sources-title">
              Sources
            </div>

            {data.sources.map((source, index) => (
              <div className="source-item" key={index}>
                {source.source || "Knowledge document"}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // Action / Revenue report
  if (
    data &&
    data.status === "success" &&
    data.result?.report
  ) {
    const report = data.result.report;

    return (
      <div className="result-card action-card">
        <div className="result-label">
          Action completed
        </div>

        <h3>{report.title}</h3>

        <div className="result-value">
          ₹{Number(report.total_revenue).toLocaleString("en-IN")}
        </div>

        <div className="result-caption">
          Total revenue
        </div>

        <div className="data-table">
          <div className="table-row table-header">
            <span>Month</span>
            <span>Revenue</span>
          </div>

          {report.monthly_revenue.map((row, index) => (
            <div className="table-row" key={index}>
              <span>{row.month}</span>

              <span>
                ₹{Number(row.revenue).toLocaleString("en-IN")}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // LangGraph wrapper response
  if (data && data.result !== undefined) {
    return <ResultCard data={data.result} />;
  }

  // Fallback
  return (
    <pre>
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendQuestion() {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/v1/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status}`
        );
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          data,
        },
      ]);
    } catch (error) {
      console.error("Aegis API error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Aegis could not process the request. Please check the API server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Aegis</h1>
          <p>AI Operations Assistant</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Ready
        </div>
      </header>

      <main className="chat">
        {messages.length === 0 && (
          <div className="welcome">
            <div className="logo">A</div>

            <h2>How can I help?</h2>

            <p>
              Ask Aegis about business data, company
              knowledge, or supported operations.
            </p>

            <div className="suggestions">
              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What is our total revenue?"
                  )
                }
              >
                Total revenue
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "Show me monthly revenue"
                  )
                }
              >
                Monthly revenue
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "Prepare a revenue report"
                  )
                }
              >
                Revenue report
              </button>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role}`}
          >
            <div className="message-label">
              {message.role === "user"
                ? "You"
                : "Aegis"}
            </div>

            {message.role === "assistant" ? (
              message.data ? (
                <ResultCard data={message.data} />
              ) : (
                <div className="user-message">
                  {message.content}
                </div>
              )
            ) : (
              <div className="user-message">
                {message.content}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-label">
              Aegis
            </div>

            <div className="user-message">
              Thinking...
            </div>
          </div>
        )}
      </main>

      <form
        className="input-area"
        onSubmit={(event) => {
          event.preventDefault();
          sendQuestion();
        }}
      >
        <input
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask Aegis..."
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading}
        >
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}

export default App;

// import { useState } from "react";

// function ResultCard({ data }) {
//   // Total revenue
//   if (
//     data &&
//     data.total_revenue !== undefined &&
//     data.status === undefined
//   ) {
//     return (
//       <div className="result-card">
//         <div className="result-label">Total Revenue</div>

//         <div className="result-value">
//           ₹{Number(data.total_revenue).toLocaleString("en-IN")}
//         </div>
//       </div>
//     );
//   }

//   // Monthly revenue
//   if (Array.isArray(data)) {
//     return (
//       <div className="result-card">
//         <div className="result-label">Monthly Revenue</div>

//         <div className="data-table">
//           <div className="table-row table-header">
//             <span>Month</span>
//             <span>Revenue</span>
//           </div>

//           {data.map((row, index) => (
//             <div className="table-row" key={index}>
//               <span>{row.month}</span>

//               <span>
//                 ₹{Number(row.revenue).toLocaleString("en-IN")}
//               </span>
//             </div>
//           ))}
//         </div>
//       </div>
//     );
//   }

//   // Knowledge / RAG
//   if (data && data.answer !== undefined) {
//     return (
//       <div className="result-card knowledge-card">
//         <div className="result-label">Knowledge</div>

//         <div className="knowledge-answer">
//           {data.answer}
//         </div>

//         {data.sources && data.sources.length > 0 && (
//           <div className="sources">
//             <div className="sources-title">
//               Sources
//             </div>

//             {data.sources.map((source, index) => (
//               <div className="source-item" key={index}>
//                 {source.source || "Knowledge document"}
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     );
//   }

//   // Action / Revenue report
//   if (
//     data &&
//     data.status === "success" &&
//     data.result?.report
//   ) {
//     const report = data.result.report;

//     return (
//       <div className="result-card action-card">
//         <div className="result-label">
//           Action completed
//         </div>

//         <h3>{report.title}</h3>

//         <div className="result-value">
//           ₹{Number(report.total_revenue).toLocaleString("en-IN")}
//         </div>

//         <div className="result-caption">
//           Total revenue
//         </div>

//         <div className="data-table">
//           <div className="table-row table-header">
//             <span>Month</span>
//             <span>Revenue</span>
//           </div>

//           {report.monthly_revenue.map((row, index) => (
//             <div className="table-row" key={index}>
//               <span>{row.month}</span>

//               <span>
//                 ₹{Number(row.revenue).toLocaleString("en-IN")}
//               </span>
//             </div>
//           ))}
//         </div>
//       </div>
//     );
//   }

//   // Fallback for unknown responses
//   return (
//     <pre>
//       {JSON.stringify(data, null, 2)}
//     </pre>
//   );
// }

// function App() {
//   const [question, setQuestion] = useState("");
//   const [messages, setMessages] = useState([]);

//   async function sendQuestion() {
//     if (!question.trim()) return;

//     const userQuestion = question;
//     const lowerQuestion = userQuestion.toLowerCase();

//     // Add user message immediately
//     setMessages((previous) => [
//       ...previous,
//       {
//         role: "user",
//         content: userQuestion,
//       },
//     ]);

//     setQuestion("");

//     // Temporary routing.
//     // This will later be replaced by LangGraph/AI routing.
//     let endpoint = "/api/v1/data/revenue";
//     let method = "GET";
//     let body = null;

//     if (lowerQuestion.includes("monthly revenue")) {
//       endpoint = "/api/v1/data/monthly-revenue";
//     } else if (
//       lowerQuestion.includes("refund") ||
//       lowerQuestion.includes("shipping") ||
//       lowerQuestion.includes("support policy")
//     ) {
//       endpoint = "/api/v1/knowledge";
//       method = "POST";

//       body = {
//         question: userQuestion,
//       };
//     } else if (lowerQuestion.includes("revenue report")) {
//       endpoint = "/api/v1/actions";
//       method = "POST";

//       body = {
//         action: "prepare_revenue_report",
//         approved: true,
//       };
//     }

//     try {
//       const options = {
//         method,
//         headers: {
//           "Content-Type": "application/json",
//         },
//       };

//       if (body) {
//         options.body = JSON.stringify(body);
//       }

//       const response = await fetch(
//         `http://127.0.0.1:8000${endpoint}`,
//         options
//       );

//       if (!response.ok) {
//         throw new Error(
//           `API request failed: ${response.status}`
//         );
//       }

//       const data = await response.json();

//       // Add structured assistant response
//       setMessages((previous) => [
//         ...previous,
//         {
//           role: "assistant",
//           data,
//         },
//       ]);
//     } catch (error) {
//       console.error("Aegis API error:", error);

//       setMessages((previous) => [
//         ...previous,
//         {
//           role: "assistant",
//           content:
//             "Unable to connect to Aegis API.",
//         },
//       ]);
//     }
//   }

//   return (
//     <div className="app">
//       <header className="header">
//         <div>
//           <h1>Aegis</h1>
//           <p>AI Operations Assistant</p>
//         </div>

//         <div className="status">
//           <span className="status-dot"></span>
//           API Ready
//         </div>
//       </header>

//       <main className="chat">
//         {messages.length === 0 && (
//           <div className="welcome">
//             <div className="logo">A</div>

//             <h2>How can I help?</h2>

//             <p>
//               Ask Aegis about business data, company
//               knowledge, or supported operations.
//             </p>

//             <div className="suggestions">
//               <button
//                 type="button"
//                 onClick={() =>
//                   setQuestion(
//                     "What is our total revenue?"
//                   )
//                 }
//               >
//                 Total revenue
//               </button>

//               <button
//                 type="button"
//                 onClick={() =>
//                   setQuestion(
//                     "Show me monthly revenue"
//                   )
//                 }
//               >
//                 Monthly revenue
//               </button>

//               <button
//                 type="button"
//                 onClick={() =>
//                   setQuestion(
//                     "Prepare a revenue report"
//                   )
//                 }
//               >
//                 Revenue report
//               </button>
//             </div>
//           </div>
//         )}

//         {messages.map((message, index) => (
//           <div
//             key={index}
//             className={`message ${message.role}`}
//           >
//             <div className="message-label">
//               {message.role === "user"
//                 ? "You"
//                 : "Aegis"}
//             </div>

//             {message.role === "assistant" ? (
//               message.data ? (
//                 <ResultCard data={message.data} />
//               ) : (
//                 <div className="user-message">
//                   {message.content}
//                 </div>
//               )
//             ) : (
//               <div className="user-message">
//                 {message.content}
//               </div>
//             )}
//           </div>
//         ))}
//       </main>

//       <form
//         className="input-area"
//         onSubmit={(event) => {
//           event.preventDefault();
//           sendQuestion();
//         }}
//       >
//         <input
//           value={question}
//           onChange={(event) =>
//             setQuestion(event.target.value)
//           }
//           placeholder="Ask Aegis..."
//         />

//         <button type="submit">
//           Send
//         </button>
//       </form>
//     </div>
//   );
// }

// export default App;

// // import { useState } from "react";

// // function ResultCard({ data }) {
// //   if (data.answer !== undefined) {
// //   return (
// //     <div className="result-card knowledge-card">
// //       <div className="result-label">
// //         Knowledge
// //       </div>

// //       <div className="knowledge-answer">
// //         {data.answer}
// //       </div>

// //       {data.sources && data.sources.length > 0 && (
// //         <div className="sources">
// //           <div className="sources-title">
// //             Sources
// //           </div>

// //           {data.sources.map((source, index) => (
// //             <div className="source-item" key={index}>
// //               {source.source || "Knowledge document"}
// //             </div>
// //           ))}
// //         </div>
// //       )}
// //     </div>
// //   );
// // }

// //   if (Array.isArray(data)) {
// //     return (
// //       <div className="result-card">
// //         <div className="result-label">Monthly Revenue</div>

// //         <div className="data-table">
// //           <div className="table-row table-header">
// //             <span>Month</span>
// //             <span>Revenue</span>
// //           </div>

// //           {data.map((row, index) => (
// //             <div className="table-row" key={index}>
// //               <span>{row.month}</span>
// //               <span>
// //                 ₹{Number(row.revenue).toLocaleString("en-IN")}
// //               </span>
// //             </div>
// //           ))}
// //         </div>
// //       </div>
// //     );
// //   }

// //   if (
// //   data.status === "success" &&
// //   data.result?.report
// // ) {
// //   const report = data.result.report;

// //   return (
// //     <div className="result-card action-card">
// //       <div className="result-label">
// //         Action completed
// //       </div>

// //       <h3>{report.title}</h3>

// //       <div className="result-value">
// //         ₹{Number(report.total_revenue).toLocaleString("en-IN")}
// //       </div>

// //       <div className="result-caption">
// //         Total revenue
// //       </div>

// //       <div className="data-table">
// //         <div className="table-row table-header">
// //           <span>Month</span>
// //           <span>Revenue</span>
// //         </div>

// //         {report.monthly_revenue.map((row, index) => (
// //           <div className="table-row" key={index}>
// //             <span>{row.month}</span>
// //             <span>
// //               ₹{Number(row.revenue).toLocaleString("en-IN")}
// //             </span>
// //           </div>
// //         ))}
// //       </div>
// //     </div>
// //   );
// // }


// //   return (
// //     <pre>
// //       {JSON.stringify(data, null, 2)}
// //     </pre>
// //   );
// // }

// // function App() {
// //   const [question, setQuestion] = useState("");
// //   const [messages, setMessages] = useState([]);

// // async function sendQuestion() {
// //   if (!question.trim()) return;

// //   const userQuestion = question;
// //   const lowerQuestion = userQuestion.toLowerCase();

// //   setMessages((previous) => [
// //     ...previous,
// //     {
// //       role: "user",
// //       content: userQuestion,
// //     },
// //   ]);

// //   setQuestion("");

// //   let endpoint = "/api/v1/data/revenue";
// // let method = "GET";
// // let body = null;

// // if (lowerQuestion.includes("monthly revenue")) {
// //   endpoint = "/api/v1/data/monthly-revenue";
// // } else if (
// //   lowerQuestion.includes("refund") ||
// //   lowerQuestion.includes("shipping") ||
// //   lowerQuestion.includes("support policy")
// // ) {
// //   endpoint = "/api/v1/knowledge";
// //   method = "POST";
// //   body = {
// //     question: userQuestion,
// //   };
// // } else if (lowerQuestion.includes("revenue report")) {
// //   endpoint = "/api/v1/actions";
// //   method = "POST";
// //   body = {
// //     action: "prepare_revenue_report",
// //     approved: true,
// //   };
// // }

// //   if (lowerQuestion.includes("monthly revenue")) {
// //     endpoint = "/api/v1/data/monthly-revenue";
// //   } else if (lowerQuestion.includes("revenue report")) {
// //     endpoint = "/api/v1/actions";
// //     method = "POST";
// //     body = {
// //       action: "prepare_revenue_report",
// //       approved: true,
// //     };
// //   }

// //   try {
// //     const options = {
// //       method,
// //       headers: {
// //         "Content-Type": "application/json",
// //       },
// //     };

// //     if (body) {
// //       options.body = JSON.stringify(body);
// //     }

// //     const response = await fetch(
// //       `http://127.0.0.1:8000${endpoint}`,
// //       options
// //     );

// //     const data = await response.json();

// //     setMessages((previous) => [
// //       ...previous,
// //       {
// //         role: "assistant",
// //         data: data,
// //       },
// //     ]);
// //   } catch (error) {
// //     setMessages((previous) => [
// //       ...previous,
// //       {
// //         role: "assistant",
// //         content: "Unable to connect to Aegis API.",
// //       },
// //     ]);
// //   }
// // }
// // //   async function sendQuestion(endpoint = "/api/v1/data/revenue", method = "GET", body = null) {
// // //   if (!question.trim()) return;

// // //   const userQuestion = question;

// // //   setMessages((previous) => [
// // //     ...previous,
// // //     {
// // //       role: "user",
// // //       content: userQuestion,
// // //     },
// // //   ]);

// // //   setQuestion("");

// // //   try {
// // //     const options = {
// // //       method,
// // //       headers: {
// // //         "Content-Type": "application/json",
// // //       },
// // //     };

// // //     if (body) {
// // //       options.body = JSON.stringify(body);
// // //     }

// // //     const response = await fetch(
// // //       `http://127.0.0.1:8000${endpoint}`,
// // //       options
// // //     );

// // //     const data = await response.json();

// // //     setMessages((previous) => [
// // //       ...previous,
// // //       {
// // //         role: "assistant",
// // //         content: JSON.stringify(data, null, 2),
// // //       },
// // //     ]);
// // //   } catch (error) {
// // //     setMessages((previous) => [
// // //       ...previous,
// // //       {
// // //         role: "assistant",
// // //         content: "Unable to connect to Aegis API.",
// // //       },
// // //     ]);
// // //   }
// // // }
// //   // async function sendQuestion() {
// //   //   if (!question.trim()) return;

// //   //   const userQuestion = question;

// //   //   setMessages((previous) => [
// //   //     ...previous,
// //   //     {
// //   //       role: "user",
// //   //       content: userQuestion,
// //   //     },
// //   //   ]);

// //   //   setQuestion("");

// //   //   try {
// //   //     const response = await fetch(
// //   //       "http://127.0.0.1:8000/api/v1/data/revenue"
// //   //     );

// //   //     const data = await response.json();

// //   //     setMessages((previous) => [
// //   //       ...previous,
// //   //       {
// //   //         role: "assistant",
// //   //         content: JSON.stringify(data, null, 2),
// //   //       },
// //   //     ]);
// //   //   } catch (error) {
// //   //     setMessages((previous) => [
// //   //       ...previous,
// //   //       {
// //   //         role: "assistant",
// //   //         content: "Unable to connect to Aegis API.",
// //   //       },
// //   //     ]);
// //   //   }
// //   // }

// //   return (
// //     <div className="app">
// //       <header className="header">
// //         <div>
// //           <h1>Aegis</h1>
// //           <p>AI Operations Assistant</p>
// //         </div>

// //         <div className="status">
// //           <span className="status-dot"></span>
// //           API Ready
// //         </div>
// //       </header>

// //       <main className="chat">
// //         {messages.length === 0 && (
// //           <div className="welcome">
// //             <div className="logo">A</div>

// //             <h2>How can I help?</h2>

// //             <p>
// //               Ask Aegis about business data, company knowledge,
// //               or supported operations.
// //             </p>

// //             <div className="suggestions">
// //   <button
// //     onClick={() => {
// //       setQuestion("What is our total revenue?");
// //     }}
// //   >
// //     Total revenue
// //   </button>

// //   <button
// //     onClick={() => {
// //       setQuestion("Show me monthly revenue");
// //     }}
// //   >
// //     Monthly revenue
// //   </button>

// //   <button
// //   onClick={() => {
// //     setQuestion("What is our refund policy?");
// //   }}
// // >
// //   Refund policy
// // </button>
// // </div>
// //           </div>
// //         )}

// //         {messages.map((message, index) => (
// //           <div
// //             key={index}
// //             className={`message ${message.role}`}
// //           >
// //             <div className="message-label">
// //               {message.role === "user" ? "You" : "Aegis"}
// //             </div>

// //             {message.role === "assistant" ? (
// //   <ResultCard data={message.data} />
// // ) : (
// //   <div className="user-message">
// //     {message.content}
// //   </div>
// // )}
// //           </div>
// //         ))}
// //       </main>

// //       <form
// //         className="input-area"
// //         onSubmit={(event) => {
// //           event.preventDefault();
// //           sendQuestion();
// //         }}
// //       >
// //         <input
// //           value={question}
// //           onChange={(event) => setQuestion(event.target.value)}
// //           placeholder="Ask Aegis..."
// //         />

// //         <button type="submit">
// //           Send
// //         </button>
// //       </form>
// //     </div>
// //   );
// // }

// // export default App;


// // //default code below:
// // // import { useState } from 'react'
// // // import heroImg from './assets/hero.png'
// // // import reactLogo from './assets/react.svg'
// // // import viteLogo from './assets/vite.svg'
// // // import './App.css'

// // // function App() {
// // //   const [count, setCount] = useState(0)

// // //   return (
// // //     <>
// // //       <section id="center">
// // //         <div className="hero">
// // //           <img src={heroImg} className="base" width="170" height="179" alt="" />
// // //           <img src={reactLogo} className="framework" alt="React logo" />
// // //           <img src={viteLogo} className="vite" alt="Vite logo" />
// // //         </div>
// // //         <div>
// // //           <h1>Get started</h1>
// // //           <p>
// // //             Edit <code>src/App.jsx</code> and save to test <code>HMR</code>
// // //           </p>
// // //         </div>
// // //         <button
// // //           type="button"
// // //           className="counter"
// // //           onClick={() => setCount((count) => count + 1)}
// // //         >
// // //           Count is {count}
// // //         </button>
// // //       </section>

// // //       <div className="ticks"></div>

// // //       <section id="next-steps">
// // //         <div id="docs">
// // //           <svg className="icon" role="presentation" aria-hidden="true">
// // //             <use href="/icons.svg#documentation-icon"></use>
// // //           </svg>
// // //           <h2>Documentation</h2>
// // //           <p>Your questions, answered</p>
// // //           <ul>
// // //             <li>
// // //               <a href="https://vite.dev/" target="_blank">
// // //                 <img className="logo" src={viteLogo} alt="" />
// // //                 Explore Vite
// // //               </a>
// // //             </li>
// // //             <li>
// // //               <a href="https://react.dev/" target="_blank">
// // //                 <img className="button-icon" src={reactLogo} alt="" />
// // //                 Learn more
// // //               </a>
// // //             </li>
// // //           </ul>
// // //         </div>
// // //         <div id="social">
// // //           <svg className="icon" role="presentation" aria-hidden="true">
// // //             <use href="/icons.svg#social-icon"></use>
// // //           </svg>
// // //           <h2>Connect with us</h2>
// // //           <p>Join the Vite community</p>
// // //           <ul>
// // //             <li>
// // //               <a href="https://github.com/vitejs/vite" target="_blank">
// // //                 <svg
// // //                   className="button-icon"
// // //                   role="presentation"
// // //                   aria-hidden="true"
// // //                 >
// // //                   <use href="/icons.svg#github-icon"></use>
// // //                 </svg>
// // //                 GitHub
// // //               </a>
// // //             </li>
// // //             <li>
// // //               <a href="https://chat.vite.dev/" target="_blank">
// // //                 <svg
// // //                   className="button-icon"
// // //                   role="presentation"
// // //                   aria-hidden="true"
// // //                 >
// // //                   <use href="/icons.svg#discord-icon"></use>
// // //                 </svg>
// // //                 Discord
// // //               </a>
// // //             </li>
// // //             <li>
// // //               <a href="https://x.com/vite_js" target="_blank">
// // //                 <svg
// // //                   className="button-icon"
// // //                   role="presentation"
// // //                   aria-hidden="true"
// // //                 >
// // //                   <use href="/icons.svg#x-icon"></use>
// // //                 </svg>
// // //                 X.com
// // //               </a>
// // //             </li>
// // //             <li>
// // //               <a href="https://bsky.app/profile/vite.dev" target="_blank">
// // //                 <svg
// // //                   className="button-icon"
// // //                   role="presentation"
// // //                   aria-hidden="true"
// // //                 >
// // //                   <use href="/icons.svg#bluesky-icon"></use>
// // //                 </svg>
// // //                 Bluesky
// // //               </a>
// // //             </li>
// // //           </ul>
// // //         </div>
// // //       </section>

// // //       <div className="ticks"></div>
// // //       <section id="spacer"></section>
// // //     </>
// // //   )
// // // }

// // // export default App
