import threading

import mysql.connector


class _MySQLConnectionManager:
  """Manager ligero para conexión MySQL.

  - Mantiene una conexión por-hilo (thread-local) para evitar reusar la misma
    conexión entre requests concurrentes.
  - Reconecta automáticamente si MySQL cerró la conexión por timeout/idle.

  Se expone como `mydb` para mantener compatibilidad con el código existente:
  `db.mydb.cursor(...)`, `db.mydb.commit()`, `db.mydb.rollback()`.
  """

  def __init__(self, **connect_kwargs):
    self._connect_kwargs = connect_kwargs
    self._state = threading.local()

  def _get_connection(self):
    conn = getattr(self._state, "conn", None)
    try:
      if conn is None or not conn.is_connected():
        conn = mysql.connector.connect(**self._connect_kwargs)
        self._state.conn = conn
    except Exception:
      # Si `is_connected()` falla por una conexión corrupta/cerrada,
      # intentamos reconstruirla.
      conn = mysql.connector.connect(**self._connect_kwargs)
      self._state.conn = conn
    return conn

  def cursor(self, *args, **kwargs):
    return self._get_connection().cursor(*args, **kwargs)

  def commit(self):
    return self._get_connection().commit()

  def rollback(self):
    return self._get_connection().rollback()

  def close(self):
    conn = getattr(self._state, "conn", None)
    if conn is not None:
      try:
        conn.close()
      finally:
        self._state.conn = None

  def is_connected(self) -> bool:
    conn = getattr(self._state, "conn", None)
    return bool(conn is not None and conn.is_connected())


mydb = _MySQLConnectionManager(
  host="localhost",
  user="root",
  password="Mart12t3.",
  database="TonerSitemas",
)