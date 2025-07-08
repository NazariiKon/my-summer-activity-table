import { useEffect, useState, useRef } from "react";

export default function Table() {
  const [days, setDays] = useState([]);
  const [categories, setCategories] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [active, setActive] = useState({ id: null, dayId: null });
  const [isEditing, setIsEditing] = useState({ id: null, dayId: null });
  const inputRef = useRef();

  function sendPostRequest(value, dayId, catId) {
    const data = {
      description: value,
      completed: true,
      day_id: dayId,
      category_id: catId,
    };
    fetch("http://127.0.0.1:8000/tasks/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => console.log("Success:", data))
      .catch((error) => console.error("Error:", error));
  }

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      const [daysRes, categoriesRes, tasksRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/day"),
        fetch("http://127.0.0.1:8000/category"),
        fetch("http://127.0.0.1:8000/tasks"),
      ]);
      const [days, categories, tasks] = await Promise.all([
        daysRes.json(),
        categoriesRes.json(),
        tasksRes.json(),
      ]);
      setDays(days);
      setCategories(categories);
      setTasks(tasks);
      setLoading(false);
    }

    fetchData();
  }, []);

  function handleMouseEnter(id, dayId) {
    setActive({ id, dayId });
  }

  function handleMouseClick(id, dayId) {
    setIsEditing({ id, dayId });
  }

  function handleKeyDown(e) {
    if (e.key == "Enter") {
      // console.log(inputRef.current.value);
      // send value to the server
      sendPostRequest(inputRef.current.value, isEditing.dayId, isEditing.id);
    }
  }

  return (
    <>
      {loading && <p>Loading...</p>}
      {!loading && (
        <table className="table table-striped table-bordered">
          <thead>
            <tr>
              <th scope="col">Date</th>
              {categories.map((categorie) => (
                <th key={categorie.id} scope="col">
                  {categorie.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {days.map((day) => (
              <tr key={day.id}>
                <th scope="row">
                  {day.date
                    .split("-")
                    .reverse()
                    .map((part, i) => (i === 2 ? part.slice(-2) : part))
                    .join(".")}
                </th>
                {categories.map((categorie) => {
                  const t = tasks.find(
                    (t) => t.category_id == categorie.id && t.day_id == day.id
                  );
                  return t != null ? (
                    <td
                      style={{ cursor: "pointer" }}
                      className={
                        active?.id == categorie.id && active?.dayId == day.id
                          ? "bg-primary"
                          : "bg-success"
                      }
                      key={categorie.id}
                      onMouseEnter={() =>
                        handleMouseEnter(categorie.id, day.id)
                      }
                      onClick={() => handleMouseClick()}
                    >
                      {t?.description}
                    </td>
                  ) : (
                    <td
                      style={{ cursor: "pointer" }}
                      key={categorie.id}
                      className={
                        active?.id == categorie.id && active?.dayId == day.id
                          ? "bg-primary"
                          : "bg-danger"
                      }
                      onMouseEnter={() =>
                        handleMouseEnter(categorie.id, day.id)
                      }
                      onClick={() => handleMouseClick(categorie.id, day.id)}
                      onBlur={() => setIsEditing(null)}
                    >
                      {isEditing?.id === categorie.id &&
                        isEditing?.dayId === day.id && (
                          <input
                            autoFocus
                            onKeyDown={handleKeyDown}
                            ref={inputRef}
                          ></input>
                        )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
