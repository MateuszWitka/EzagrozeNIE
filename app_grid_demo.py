import streamlit as st
import re
import pandas as pd


class Square:

    def __init__(self, data = None, y = [None, None], x = [None, None]):

        self.data = data
        self.y = y
        self.x = x
        self.down = None
        self.up = None
        self.left = None
        self.right = None



class Grid:

    def __init__(self, data = None, unit = None, y = [None, None], x = [None, None]):

        self.data = data
        self.unit = unit
        self.y = y
        self.x = x
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.root = Square(y = [(self.y[0] + self.y[1])/2 - self.unit/2, (self.y[0] + self.y[1])/2 + self.unit/2], x = [(self.x[0] + self.x[1])/2 - self.unit/2, (self.x[0] + self.x[1])/2 + self.unit/2])

    def build_grid(self):

        current_horizontal = self.root
        while (current_horizontal.x[1] < self.x[1]):
            new_horizontal = Square(y = current_horizontal.y, x = [current_horizontal.x[0] + self.unit, current_horizontal.x[1] + self.unit])
            new_horizontal.left = current_horizontal
            current_horizontal.right = new_horizontal

            current_vertical = current_horizontal
            while (current_vertical.y[1] < self.y[1]):
                new_vertical = Square(x = current_vertical.x, y = [current_vertical.y[0] + self.unit, current_vertical.y[1] + self.unit])
                new_vertical.down = current_vertical
                current_vertical.up = new_vertical
                current_vertical = new_vertical

            current_horizontal = new_horizontal




test_grid = Grid(y = [51.36333333333334, 53.12388888888889], x = [14.534166666666668, 16.416666666666668], unit = 1/3600)

test_grid.build_grid()



dataframe = pd.read_csv(r'C:\Users\Lenovo\Desktop\systemy informatyczne\ćw 7\wypadki_lubuskie_2024.csv', index_col = 0)



current_square = test_grid.root


for i in range(14):
    next_square = current_square.right
    current_square = next_square


for i in range(34):
    next_square = current_square.up
    current_square = next_square


current_square.data = dataframe[(dataframe['gps_x'] <= current_square.x[1]) & (dataframe['gps_x'] > current_square.x[0]) & (dataframe['gps_y'] <= current_square.y[1]) & (dataframe['gps_y'] > current_square.y[0])]



st.title('Demonstracja struktury siatki')


st.write('Rozpiętość siatki województwa:')
st.write(f'x: {test_grid.x[0]}° - {test_grid.x[1]}°')
st.write(f'y: {test_grid.y[0]}° - {test_grid.y[1]}°')

st.write('\n\n')

st.write('Koordynaty wybranego kwadratu')
st.write(f'x: {current_square.x[0]}° - {current_square.x[1]}°')
st.write(f'y: {current_square.y[0]}° - {current_square.y[1]}°')

st.write('\n\n')

st.write(f'Jednostka długości (granulacja danych) wynosi jedną sekundę, a zatem {test_grid.unit} stopnia.')

st.write('\n\n')

st.write('Koordynaty górnego sąsiada wybranego kwadratu (na północ)')
st.write(f'x: {current_square.up.x[0]}° - {current_square.up.x[1]}°')
st.write(f'y: {current_square.up.y[0]}° - {current_square.up.y[1]}°')

st.write('\n\n')

st.write('Koordynaty dolnego sąsiada poprzedniego kwadratu (na południe)')
st.write(f'x: {current_square.down.x[0]}° - {current_square.down.x[1]}°')
st.write(f'y: {current_square.down.y[0]}° - {current_square.down.y[1]}°')

st.write('\n\n')

st.write('Dane zawarte w aktualnym kwadracie:')
current_square.data

