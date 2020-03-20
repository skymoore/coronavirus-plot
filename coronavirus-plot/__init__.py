import csv, requests
import matplotlib.pyplot as plt
from consolemenu import SelectionMenu
from .coronaVars import csv_urls, lil_key, big_key



def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))


def plot_data(csv_url_key, choice):

    data_file = get_file(csv_urls[csv_url_key])

    for row in data_file:

        if row[lil_key] == choice[lil_key] and row[big_key] == choice[big_key]:

            y_axis = [int(row[num]) for num in row if (row[num].isnumeric() and int(row[num]) > 0)]

            x_axis = data_file.fieldnames[-len(y_axis):]
            x_axis = [ x_axis[i] for i in range(len(y_axis)) ]

            if len(x_axis) == len(y_axis) and len(y_axis) > 0:
                print(f'plotting {csv_url_key} cases')
                plt.plot(x_axis, y_axis, label=csv_url_key)

                for i, v in zip(x_axis, y_axis):
                    plt.text(i, v, str(v))
            else:
                print(f'no {csv_url_key} cases reported')


def main():

    print("Welcome to the Corona Data CLI")
    input("Press any key to select a location...")
    # get list of available locations
    data_response = get_file(csv_urls['confirmed'])

    choices = []
    choices_strings = []

    for row in data_response:

        if row[big_key] != '' and row[lil_key].count(',') == 0:
            choices.append( { lil_key: row[lil_key], big_key: row[big_key] } )

            if row[lil_key] == '':
                choices_strings.append(row[big_key])

            else:
                choices_strings.append(row[lil_key] + ' - ' + row[big_key])
    
    # have user choose location
    choices_map = { choices_strings[i] : i for i in range(len(choices)) }
    choices_strings.sort()
    index = SelectionMenu.get_selection(choices_strings, title=lil_key)
    if index >= len(choices):
        exit()
    choice = choices[choices_map[choices_strings[index]]]

    # show feedback
    if choice[lil_key] == '':
        print('Building plot for',choice[big_key])

    else:
        print('Building plot for',choice[lil_key],' - ',choice[big_key])

    # plot the data
    for csv_url in csv_urls:
        plot_data(csv_url, choice)

    # configure the figure and show the plot
    plt.xlabel('date')
    plt.ylabel('count')
    if choice[lil_key] == '':
        plt.title(choice[big_key])

    else:
        plt.title(choice[lil_key] + ' ' + choice[big_key])

    plt.legend()
    plt.show()


main()
