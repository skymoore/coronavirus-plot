import csv, requests
import matplotlib.pyplot as plt
from consolemenu import SelectionMenu
from .coronaVars import csv_urls, lil_key, big_key



def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))


def plot_data(csv_url_key, plot, choice):
    returned_plot = None
    data_file = get_file(csv_urls[csv_url_key])

    for row in data_file:

        if row[lil_key] == choice[lil_key] and row[big_key] == choice[big_key]:

            y_axis = [int(row[num]) for num in row if (row[num].isnumeric() and int(row[num]) > 0)]

            x_axis = data_file.fieldnames[-len(y_axis):]
            x_axis = [ x_axis[i] for i in range(len(y_axis)) ]

            if len(x_axis) == len(y_axis) and len(y_axis) > 0:
                print(f'plotting {csv_url_key} cases')
                returned_plot, = plot.plot(x_axis, y_axis, label=csv_url_key)

                for x, y in zip(x_axis, y_axis):
                    plot.text(x, y, str(y))
            else:
                print(f'no {csv_url_key} cases reported')
    
    return returned_plot


def main():
    figures = []
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
        if choice[lil_key] == '':
            fig = plt.figure(num=csv_url + ' cases in ' + choice[big_key])
        else:
            fig = plt.figure(num=csv_url + ' cases in ' + choice[lil_key] + ' - ' + choice[big_key])

        if choice[lil_key] == '':
            plot = fig.add_subplot(1,1,1,
                                   title=choice[big_key],
                                   xlabel='date',
                                   ylabel='number of cases')

        else:
            plot = fig.add_subplot(1,1,1,
                                   title=choice[lil_key] + ' ' + choice[big_key],
                                   xlabel='date',
                                   ylabel='number of cases')

        the_plot = plot_data(csv_url, plot, choice)
        if the_plot is not None:
            # configure the figure and show the plot
            plot.set_label(csv_url)
            plot.legend()
            fig.show()
        figures.append(fig)


    input("Press any key to continue, plots will be closed...")
        
    for a_fig in figures:
        plt.close(a_fig)
        
    figures.clear()

if __name__ == '__main__':
    main()   
