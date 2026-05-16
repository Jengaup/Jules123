# Sistema de Contabilidad y Finanzas para Iglesias en Puerto Rico

Este es un sistema basado en Flask para administrar la contabilidad y las finanzas de una iglesia en Puerto Rico, diseñado para cumplir con los requisitos de precisión financiera y las particularidades fiscales locales (como la exención de vivienda para ministros).

## Características

- **Autenticación:** Acceso protegido para el administrador.
- **Precisión Financiera:** Uso de `Decimal` y `Numeric` para evitar errores de redondeo en moneda.
- **Ingresos y Gastos:** Registro detallado por categorías (Diezmos, Ofrendas, Misiones, Servicios, etc.).
- **Compensación de Ministros:** Manejo separado de Salario Base y Asignación de Vivienda/Servicios (Exento según Hacienda PR).
- **Dashboard:** Visualización rápida de totales y balance actual.

## Instalación y Uso

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Inicializar la base de datos:**
   (Crea el usuario `admin` con contraseña `admin123` y las categorías iniciales).
   ```bash
   python3 init_db.py
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python3 app.py
   ```

4. **Acceder:**
   Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador.

## Credenciales por defecto
- **Usuario:** `admin`
- **Contraseña:** `admin123`
