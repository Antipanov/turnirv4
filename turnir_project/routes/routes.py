from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from sqlalchemy import desc
from ..models.models import ParticipantsDB, FightsDB
from ..extensions import db
import csv

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_view():
    return render_template("home.html")


@home.route('/fill_fighters')
def fill_fighters():
    with open('fighters.csv', encoding='utf8') as csvfile:
        fighters_csv_list = csv.reader(csvfile)
        for row in fighters_csv_list:
            new_fighter = ParticipantsDB(participant_first_name=row[0], participant_last_name=row[1], activity_status=1)
            db.session.add(new_fighter)
            try:
                db.session.commit()
                print("Бойцы импортированы в базу")
            except Exception as e:
                print("Не получилось импортировать бойцов. Ошибка: ", e)
                db.session.rollback()
    return "результат импорта - в принт"


def fight_create_func(round_number):
    round_number = int(round_number)
    # Список id активных бойцов
    active_fighters_id_data = db.session.query(ParticipantsDB.participant_id).filter_by(activity_status=1).all()
    active_fighters_id_list = [value for value, in active_fighters_id_data]

    # Список красных бойцов, которые уже есть в текущем раунде
    red_fighters_fights_data = db.session.query(FightsDB.red_fighter_id).filter_by(round_number=round_number).all()
    red_fighters_id_list = [value for value, in red_fighters_fights_data]
    # Список синих бойцов, которые уже есть в текущем раунде
    blue_fighters_fights_data = db.session.query(FightsDB.blue_fighter_id).filter_by(round_number=round_number).all()
    blue_fighters_id_list = [value for value, in blue_fighters_fights_data]
    # список всех бойцов, которые уже есть в текущем раунде
    fighters_id_list = red_fighters_id_list + blue_fighters_id_list
    # список бойцов, которые активны, но еще не в текущем раунде
    free_fighters_list = list(set(active_fighters_id_list) - set(fighters_id_list))
    # если количество свободных бойцов больше одного, то берем первых двух из списка и добавляем их в красного и синего
    if len(free_fighters_list) > 1:
        red_fighter_id = free_fighters_list[0]
        blue_fighter_id = free_fighters_list[1]
        new_fight = FightsDB(round_number=round_number, red_fighter_id=red_fighter_id,
                             blue_fighter_id=blue_fighter_id)
        db.session.add(new_fight)
        try:
            db.session.commit()

            print("создан новый бой в круге №", round_number, ". id бойцов:", red_fighter_id, " и ", blue_fighter_id)
        except Exception as e:
            print("не получилось создать новый бой. Ошибка:  ", e)
            db.session.rollback()
    else:
        round_number = round_number + 1
    return round_number

@home.route('/competition')
def competition_start():
  # создаем первый бой
  fight_create_func(1)
  # last_created_fight = FightsDB.query.order_by(desc(FightsDB.fight_id)).first()
  return redirect(url_for('home.competition_view', round_no=1))

@home.route('/competition/<int:round_no>')
def competition_view(round_no):
    round_number_prev = round_no
    # round_number = fight_create_func(round_number_prev)
    last_created_fight = FightsDB.query.order_by(desc(FightsDB.fight_id)).first()
    print("id последнего созданного боя", last_created_fight.fight_id)
    return render_template("competition.html", fight_data=last_created_fight)


@home.route('/ajaxfile_red_fighter', methods=["POST", "GET"])
def ajaxfile_red_fighter():
    if request.method == 'POST':
      fight_id = request.form['fight_id']
      print("fight_id после нажатия", fight_id)

      # выводим из игры синего бойца
      # current_fight_data = db.session.query(FightsDB).filter_by(fight_id=fight_id).all()[0]
      # print("на удаление ", current_fight_data.blue_fighter.participant_last_name)
      # current_fight_data.blue_fighter.activity_status = 0
      # try:
      #   db.session.commit()
      # except Exception as e:
      #   print("не удалось обновить статус проигравшего", e)
      #   db.session.rollback()
      # создаем новый бой 
      fight_create_func(1)
      last_created_fight = FightsDB.query.order_by(desc(FightsDB.fight_id)).first()
      print("id последнего созданного боя", last_created_fight.fight_id)

      return jsonify({'htmlresponsered': render_template('response_red_fighter_div.html', fight_data=last_created_fight),
                     'htmlresponseblue': render_template('response_blue_fighter_div.html', fight_data=last_created_fight)
                     })
