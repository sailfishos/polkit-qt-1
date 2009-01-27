/*
 * This file is part of the Polkit-qt project
 * Copyright (C) 2009 Daniel Nicoletti <dantti85-pk@yahoo.com.br>
 * Copyright (C) 2009 Dario Freddi <drf54321@gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public License
 * along with this library; see the file COPYING.LIB. If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#include "QPkActionButton.h"

#include <QtCore/QDebug>

using namespace QPolicyKit;

class ActionButton::Private
{
    public:
        Private(QAbstractButton *b)
         : button(b)
         , initiallyChecked(false)
        {};

        QAbstractButton *button;
        bool initiallyChecked;
};

ActionButton::ActionButton(QAbstractButton *button, const QString &actionId, QWidget *parent)
 : Action(actionId, parent)
 , d(new Private(button))
{
    connect(this, SIGNAL(dataChanged()), SLOT(updateButton()));
    if (d->button->isCheckable()) {
        d->initiallyChecked = d->button->isChecked();
        // we track the clicked signal to not enter in an
        // infinete loop as setChecked() would call toggled over
        // and over...
        connect(d->button, SIGNAL(clicked()), SLOT(toggled()));
    } else {
        connect(d->button, SIGNAL(clicked()), SLOT(activateProxy()));
    }
    // call this after m_activateOnCheck receives the value
    updateButton();
}

void ActionButton::updateButton()
{
    qDebug() << "ActionButton::updateButton()";
    d->button->setVisible(visible());
    d->button->setEnabled(enabled());
    // We check for Null to see if the user
    // never set anything as "" is not NULL
    if (!text().isNull()) {
        d->button->setText(text());
    }
    if (!toolTip().isNull()) {
        d->button->setToolTip(toolTip());
    }
    if (!whatsThis().isNull()) {
        d->button->setWhatsThis(whatsThis());
    }
    if (!icon().isNull()) {
        d->button->setIcon(icon());
    }
    // if the item cannot do the action anymore
    // lets revert to the initial state
    if (d->button->isCheckable() && !canDoAction()) {
        d->button->setChecked(d->initiallyChecked);
    }
}

void ActionButton::activateProxy()
{
    activate(d->button->winId());
}

void ActionButton::toggled()
{
    qDebug() << "toggle";
    // We store the value cause it might create an
    // event loop that can conflict with our desired
    // value.
    bool checked = d->button->isChecked();
    // we set the the opposite option in case the activate fails
    if (activate(d->button->winId())) {
        d->button->setChecked(checked);
    } else {
        // don't undo the checked before
        // you call activate because the
        // activated signal is emmited from there
        // and the user will see the wrong checked state
        d->button->setChecked(!checked);
    }
}