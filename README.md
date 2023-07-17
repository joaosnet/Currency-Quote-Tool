# Currency Quote Tool - Python with Tkinter

This repository contains a currency quotation tool developed in Python using Tkinter. It provides a graphical user interface (GUI) for users to retrieve currency exchange rates.

## Dependencies

The following Python libraries are required to run the tool:

- `tkinter` (imported as `tk`): Used for GUI development.
- `requests` (imported as `rq`): Used for making HTTP requests to fetch currency data.
- `pandas` (imported as `pd`): Used for data manipulation and analysis.
- `numpy` (imported as `np`): Used for numerical computations.
- `ttk` from `tkinter`: Used for additional Tkinter widgets.
- `DateEntry` from `tkcalendar`: Used for selecting dates.
- `askopenfilename` from `tkinter.filedialog`: Used for selecting files.
- `datetime` module: Used for date and time operations.

## Usage

1. Ensure that you have Python installed on your system.
2. Install the required dependencies by running the following command:

```shell
pip install tkinter requests pandas numpy tkcalendar
```

3. Clone this repository or download the source code.
4. Navigate to the project directory.
5. Run the following command to start the currency quotation tool:

```shell
python currency_quote_tool.py
```

6. The GUI will open, allowing you to select currencies, dates, and other options.
7. Click on the "Get Quote" button to retrieve the currency exchange rates.
8. The results will be displayed in the GUI, and you can also choose to save them to a file using the "Save Results" button.

## Screenshots

![Currency Quote Tool](/screenshots/currency_quote_tool.png)

_Figure 1: Currency Quote Tool GUI_


 
